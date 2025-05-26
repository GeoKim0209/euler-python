#!/usr/bin/env python
import http.server
import os
import shutil
import socketserver
import subprocess
import webbrowser
from pathlib import Path


def main():
    # Find uv executable
    uv_path = shutil.which("uv")
    if not uv_path:
        print("Error: 'uv' not found in PATH. Please install it using 'pip install uv'.")
        return

    # Generate the site with local flag
    print("Generating site for local development...")
    subprocess.run(
        [uv_path, "run", os.path.join(os.path.dirname(__file__), "generate_site.py"), "--local"]
    )

    # Start a local server
    PORT = 8000
    DIRECTORY = Path(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) / "site"

    if not DIRECTORY.exists():
        print(
            f"Error: '{DIRECTORY}' directory not found. Make sure the site was generated correctly."
        )
        return

    print(f"Starting server at http://localhost:{PORT}")

    class Handler(http.server.SimpleHTTPRequestHandler):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, directory=str(DIRECTORY), **kwargs)

        def end_headers(self):
            # Add headers required for SharedArrayBuffer support (needed for Pyodide timeout functionality)
            self.send_header("Cross-Origin-Opener-Policy", "same-origin")
            self.send_header("Cross-Origin-Embedder-Policy", "require-corp")
            super().end_headers()

    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        # Open browser
        webbrowser.open(f"http://localhost:{PORT}")

        # Serve until interrupted
        try:
            print("Press Ctrl+C to stop the server")
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nServer stopped")


if __name__ == "__main__":
    main()
