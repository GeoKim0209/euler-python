# /// script
# requires-python = ">=3.8"
# dependencies = [
#   "jinja2==3.1.2",
#   "pygments==2.15.1",
#   "markupsafe",
#   "pillow",
# ]
# ///

import datetime
import os
import re
import shutil
import sys
from pathlib import Path

import pygments
from jinja2 import Environment, FileSystemLoader
from markupsafe import Markup
from PIL import Image
from pygments.formatters import HtmlFormatter
from pygments.lexers import get_lexer_by_name

# Check if running in local development mode
is_local = len(sys.argv) > 1 and sys.argv[1] == "--local"

# Site configuration
site_config = {
    "title": "Project Euler Solutions",
    "description": "Solutions to Project Euler problems in Python",
    "author": "Geo Kim",
    "github_repo": "https://github.com/GeoKim0209/euler-python",
    "base_url": "" if is_local else "/euler-python",
}

# Directory structure
ROOT_DIR = Path(os.path.dirname(os.path.abspath(__file__))).parent
SOLUTIONS_DIR = ROOT_DIR / "solutions"
TEMPLATES_DIR = ROOT_DIR / "web" / "templates"
OUTPUT_DIR = ROOT_DIR / "site"
ASSETS_DIR = OUTPUT_DIR / "assets"
FAVICON_DIR = ASSETS_DIR / "favicon"
PROBLEMS_DIR = OUTPUT_DIR / "problems"
STYLE_FILE = ROOT_DIR / "web" / "style.css"
STYLE_EXTRA_FILE = ROOT_DIR / "web" / "style_extra.css"
LOGO_FILE = ROOT_DIR / "web" / "geo_logo.png"

# Create necessary directories
os.makedirs(TEMPLATES_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(ASSETS_DIR / "css", exist_ok=True)
os.makedirs(FAVICON_DIR, exist_ok=True)
os.makedirs(PROBLEMS_DIR, exist_ok=True)


# Extract problem number from filename (p1.py -> 1)
def get_problem_number(filename):
    match = re.match(r"p(\d+)\.py", filename)
    if match:
        return int(match.group(1))
    return None


# Remove HTML tags from text
def strip_html_tags(text):
    return re.sub(r"<[^>]+>", "", text)


# Parse problem solutions
def parse_solution_file(file_path):
    with open(file_path, "r") as f:
        content = f.read()

    # Look for a single-line comment at the top of the file
    first_line = content.split("\n")[0].strip()
    top_comment = None
    if first_line.startswith("# "):
        top_comment = first_line[2:].strip()  # Remove the "# " prefix

    # Extract problem statement from docstring - support both """ and ''' formats
    statement_match = re.search(r'("""|\'\'\')(.*?)\1', content, re.DOTALL)
    statement = statement_match.group(2).strip() if statement_match else ""

    # Get problem title preferring the top comment if it exists
    if top_comment:
        title = top_comment
    else:
        # Fall back to the first paragraph if no top comment
        title_match = re.search(r"<p>(.*?)</p>", statement)
        title = (
            title_match.group(1) if title_match else f"Problem {get_problem_number(file_path.name)}"
        )

        # Clean up title - extract main concept
        title = strip_html_tags(title)  # Remove HTML tags
        title = re.sub(r"\$.*?\$", "", title)  # Remove math expressions
        title = " ".join(title.split()[:4])  # Take first few words
        title = title.split(".")[0].strip()

    return {
        "number": get_problem_number(file_path.name),
        "filename": file_path.name,
        "title": title,
        "statement": statement,
        "solution": content,
    }


# Get list of all problems
def get_all_problems():
    problem_files = sorted(
        [
            f
            for f in os.listdir(SOLUTIONS_DIR)
            if f.startswith("p") and f.endswith(".py") and get_problem_number(f) is not None
        ],
        key=lambda x: get_problem_number(x),
    )
    problems = []

    for filename in problem_files:
        file_path = SOLUTIONS_DIR / filename
        problem_data = parse_solution_file(file_path)
        problems.append(problem_data)

    return problems


# Define a simple "now" function for Jinja2
def get_current_year():
    return datetime.datetime.now().year


# Set up Jinja environment
env = Environment(loader=FileSystemLoader(TEMPLATES_DIR))
env.globals["current_year"] = get_current_year()


# Function to mark content as safe in templates
def safe_content(content):
    return Markup(content)


env.filters["safe_content"] = safe_content


# Function to generate favicon files
def generate_favicons():
    if not os.path.exists(LOGO_FILE):
        print(f"Warning: Logo file {LOGO_FILE} not found. Skipping favicon generation.")
        return

    # Create favicon directory if it doesn't exist
    os.makedirs(FAVICON_DIR, exist_ok=True)

    # Load the logo image
    with Image.open(LOGO_FILE) as img:
        # Generate favicons of different sizes
        favicon_sizes = [16, 32, 48, 180, 192, 512]
        for size in favicon_sizes:
            favicon = img.copy()
            favicon = favicon.resize((size, size), Image.Resampling.LANCZOS)

            # Save as PNG
            favicon.save(FAVICON_DIR / f"favicon-{size}x{size}.png", "PNG")

            # For the standard favicon.ico, save the 32x32 version
            if size == 32:
                favicon.save(FAVICON_DIR / "favicon.ico", "ICO")

        # Save original as apple-touch-icon.png (180x180)
        apple_icon = img.copy()
        apple_icon = apple_icon.resize((180, 180), Image.Resampling.LANCZOS)
        apple_icon.save(FAVICON_DIR / "apple-touch-icon.png", "PNG")

    print(f"Favicon files generated in {FAVICON_DIR}")


# Generate the site
def generate_site():
    # Clean output directory (but keep assets if exists)
    if os.path.exists(PROBLEMS_DIR):
        shutil.rmtree(PROBLEMS_DIR)
    os.makedirs(PROBLEMS_DIR, exist_ok=True)

    # Generate favicons
    generate_favicons()

    # Get all problems
    problems = get_all_problems()

    # Generate CSS files
    with open(ASSETS_DIR / "css" / "style.css", "w") as f:
        # Base CSS styles
        with open(STYLE_FILE, "r") as css_file:
            css = css_file.read()

        # Add Pygments syntax highlighting CSS
        pygments_css = HtmlFormatter(style="default").get_style_defs(".highlight")
        css += "\n\n" + pygments_css

        # Add extra styles from style_extra.css if it exists
        if os.path.exists(STYLE_EXTRA_FILE):
            with open(STYLE_EXTRA_FILE, "r") as extra_css_file:
                extra_css = extra_css_file.read()
                css += "\n\n/* Extra styles */\n" + extra_css

        f.write(css)

    # Parse Euler library functions
    def parse_euler_library():
        euler_path = ROOT_DIR / "euler" / "__init__.py"
        with open(euler_path, "r") as f:
            content = f.read()

        # Extract functions
        functions = []

        # Get all lines in the file
        lines = content.split("\n")

        i = 0
        while i < len(lines):
            line = lines[i].strip()

            # Check if this is a function definition
            match = re.match(r"def\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*\((.*?)\):", line)
            if match:
                func_name = match.group(1)
                func_params = match.group(2)

                # Start collecting the function body
                func_body = [line]

                # Track indentation of the function definition
                base_indent = len(lines[i]) - len(lines[i].lstrip())

                # Move to next line
                i += 1

                # Continue collecting until we reach a line with same or less indentation
                # that isn't blank or a comment
                while i < len(lines):
                    curr_line = lines[i]
                    curr_stripped = curr_line.strip()

                    # Skip empty lines
                    if not curr_stripped:
                        func_body.append(curr_line)
                        i += 1
                        continue

                    # Check indentation level
                    curr_indent = len(curr_line) - len(curr_line.lstrip())

                    # If we've reached a line with same or less indentation that's not a comment,
                    # we've exited the function
                    if curr_indent <= base_indent and not curr_stripped.startswith("#"):
                        break

                    # Add line to function body
                    func_body.append(curr_line)
                    i += 1

                # Join the function body
                full_func_code = "\n".join(func_body)

                # Extract docstring if present
                docstring = ""
                docstring_match = re.search(r'("""|\'\'\')(.*?)\1', full_func_code, re.DOTALL)
                if docstring_match:
                    docstring = docstring_match.group(2).strip()
                    full_func_code = re.sub(r'    ("""|\'\'\')(.*?)\1\n', "", full_func_code)

                # Generate description
                if not docstring:
                    description = f"Function that {func_name.replace('_', ' ')}."
                else:
                    description = docstring

                # Highlight code
                lexer = get_lexer_by_name("python", stripall=True)
                formatter = HtmlFormatter(cssclass="highlight")
                highlighted_code = pygments.highlight(full_func_code, lexer, formatter)

                functions.append(
                    {"name": func_name, "description": description, "code": highlighted_code}
                )
            else:
                i += 1

        return functions

    # Generate problem pages
    for i, problem in enumerate(problems):
        # Create problem directory
        problem_dir = PROBLEMS_DIR / f"problem-{problem['number']}"
        os.makedirs(problem_dir, exist_ok=True)

        # Find previous and next problems
        prev_problem = problems[i - 1] if i > 0 else None
        next_problem = problems[i + 1] if i < len(problems) - 1 else None

        # Highlight code
        lexer = get_lexer_by_name("python", stripall=True)
        formatter = HtmlFormatter(cssclass="highlight")
        highlighted_code = pygments.highlight(problem["solution"], lexer, formatter)

        # Render problem page
        template = env.get_template("problem.html")
        output = template.render(
            site_config=site_config,
            problem=problem,
            prev_problem=prev_problem,
            next_problem=next_problem,
            highlighted_code=highlighted_code,
        )

        with open(problem_dir / "index.html", "w") as f:
            f.write(output)

    # Generate index page
    template = env.get_template("index.html")
    output = template.render(site_config=site_config, problems=problems)

    with open(OUTPUT_DIR / "index.html", "w") as f:
        f.write(output)

    # Generate Euler library page
    euler_functions = parse_euler_library()
    template = env.get_template("euler_library.html")
    output = template.render(site_config=site_config, euler_functions=euler_functions)

    os.makedirs(OUTPUT_DIR / "euler-library", exist_ok=True)
    with open(OUTPUT_DIR / "euler-library" / "index.html", "w") as f:
        f.write(output)

    print(f"Site generated successfully in {OUTPUT_DIR}")


if __name__ == "__main__":
    if is_local:
        print("Generating site for local development (no base URL)")
    generate_site()
