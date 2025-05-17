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
        css = """
.site-header .container {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.site-logo {
  width: 64px;
  height: 64px;
}

:root {
    --primary-color: #0366d6;
    --secondary-color: #586069;
    --bg-color: #ffffff;
    --text-color: #24292e;
    --light-bg: #f6f8fa;
    --border-color: #e1e4e8;
    --color-red: #d73a49;
    --color-green: #28a745;
    --color-blue: #0366d6;
    --color-light-blue: #79b8ff;
    --color-orange: #e36209;
    --color-dark-green: #22863a;
    --color-border-default: #e1e4e8;
    --color-text-link: #0366d6;
    --font-monospace: SFMono-Regular, Consolas, Liberation Mono, Menlo, monospace;
}

* {
    box-sizing: border-box;
    margin: 0;
    padding: 0;
}

body {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
    line-height: 1.6;
    color: var(--text-color);
    background-color: var(--bg-color);
}

.container {
    width: 100%;
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 20px;
}

/* Header Styles */
.site-header {
    background-color: var(--primary-color);
    padding: 15px 0;
    color: white;
}

.site-header .container {
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.site-title {
    font-size: 1.5rem;
    font-weight: bold;
    color: white;
    text-decoration: none;
}

.site-nav {
    display: flex;
    gap: 20px;
}

.site-nav a {
    color: white;
    text-decoration: none;
}

.site-nav a:hover {
    text-decoration: underline;
}

/* Main Content Styles */
.page-content {
    padding: 40px 0;
    min-height: calc(100vh - 132px);
}

h1 {
    margin-bottom: 20px;
}

h2 {
    margin: 30px 0 15px;
}

p {
    margin-bottom: 15px;
}

a {
    color: var(--primary-color);
    text-decoration: none;
}

a:hover {
    text-decoration: underline;
}

/* Footer Styles */
.site-footer {
    background-color: var(--light-bg);
    padding: 20px 0;
    border-top: 1px solid var(--border-color);
}

.site-footer p {
    color: var(--secondary-color);
    text-align: center;
    margin: 0;
}

/* Problem Table Styles */
.problem-table-container {
    margin-top: 30px;
    overflow-x: auto;
}

.problem-table {
    width: 100%;
    border-collapse: collapse;
    border-spacing: 0;
}

.problem-table th,
.problem-table td {
    padding: 12px 15px;
    text-align: left;
    border-bottom: 1px solid var(--border-color);
}

.problem-table th {
    background-color: var(--light-bg);
    font-weight: bold;
    color: var(--text-color);
}

.problem-row {
    cursor: pointer;
    transition: background-color 0.2s;
}

.problem-row:hover {
    background-color: var(--light-bg);
}

.problem-row:hover td:first-child a {
    color: red;
}

.problem-row:hover .problem-title {
    color: red;
}

.problem-number a {
    text-decoration: none;
    color: var(--primary-color);
    font-weight: bold;
}

.problem-number a:hover {
    text-decoration: underline;
}

.problem-title {
    color: var(--text-color);
}

/* Problem Grid Styles - Kept for backwards compatibility */
.problem-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
    gap: 20px;
    margin-top: 30px;
}

.problem-card {
    padding: 15px;
    border-radius: 5px;
    background-color: var(--light-bg);
    border: 1px solid var(--border-color);
    transition: transform 0.2s, box-shadow 0.2s;
}

.problem-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 10px 20px rgba(0,0,0,0.1);
}

.problem-card h3 {
    margin-top: 0;
    margin-bottom: 10px;
}

.problem-card h3 a {
    text-decoration: none;
    color: var(--primary-color);
}

/* Problem Page Styles */
.problem-page {
    max-width: 800px;
    margin: 0 auto;
    padding: 20px;
}

.problem-navigation {
    margin-bottom: 30px;
    position: relative;
}

.home-link {
    display: inline-block;
    margin-bottom: 10px;
    text-decoration: none;
    color: var(--primary-color);
}

.nav-buttons {
    display: flex;
    justify-content: space-between;
    margin-top: 20px;
}

.nav-button {
    padding: 5px 10px;
    text-decoration: none;
    background-color: var(--light-bg);
    border-radius: 4px;
    color: var(--text-color);
}

.problem-statement,
.problem-solution {
    margin-bottom: 30px;
    background-color: var(--light-bg);
    padding: 20px;
    border-radius: 5px;
    border-left: 4px solid var(--primary-color);
}

.statement-content {
    line-height: 1.6;
}

.code-container {
    margin-top: 15px;
    overflow-x: auto;
}

pre {
    padding: 15px;
    border-radius: 5px;
    font-size: 14px;
}

/* Euler Library Page */
.euler-library {
    background-color: var(--light-bg);
    padding: 20px;
    border-radius: 5px;
    margin-top: 20px;
    border-left: 4px solid var(--primary-color);
}

.euler-function {
    margin-bottom: 30px;
}

.euler-function h3 {
    color: var(--primary-color);
    margin-bottom: 10px;
}

.function-description {
    margin-bottom: 15px;
}

/* Code highlighting */
.highlight pre {
    background-color: #f8f8f8;
    border: 1px solid #e1e4e8;
    border-radius: 4px;
    line-height: 1.45;
    overflow: auto;
    padding: 16px;
}

/* Responsive styles */
@media (max-width: 768px) {
    .site-header .container {
        flex-direction: column;
        align-items: flex-start;
    }
    
    .site-nav {
        margin-top: 10px;
    }
    
    .problem-grid {
        grid-template-columns: 1fr;
    }
    
    .problem-table th,
    .problem-table td {
        padding: 8px 10px;
    }
    
    .problem-table {
        font-size: 0.95em;
    }
}

/* MathJax Styling */
.MathJax {
    font-size: 1.1em !important;
}

.statement-content {
    font-size: 1.05em;
}

.statement-content p {
    margin-bottom: 1.2em;
}

/* Ensure math expressions are properly spaced */
.statement-content .MathJax_Display {
    margin: 1em 0;
}
"""
        # Add Pygments syntax highlighting CSS
        pygments_css = HtmlFormatter(style="default").get_style_defs(".highlight")
        css += "\n\n" + pygments_css

        # Add extra styles from style_extra.css if it exists
        if os.path.exists(STYLE_EXTRA_FILE):
            with open(STYLE_EXTRA_FILE, "r") as extra_css_file:
                extra_css = extra_css_file.read()
                css += "\n\n/* Extra styles */\n" + extra_css

        f.write(css)

    # Generate index page
    with open(TEMPLATES_DIR / "base.html", "w") as f:
        f.write("""<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>
      {% block title %}{{ site_config.title }}{% endblock %}
    </title>
    <link
      rel="stylesheet"
      href="{{ site_config.base_url }}/assets/css/style.css"
    />
    <!-- Favicon links -->
    <link rel="icon" type="image/png" href="{{ site_config.base_url }}/assets/favicon/favicon.ico" />
    <link rel="icon" type="image/png" sizes="32x32" href="{{ site_config.base_url }}/assets/favicon/favicon-32x32.png" />
    <link rel="icon" type="image/png" sizes="16x16" href="{{ site_config.base_url }}/assets/favicon/favicon-16x16.png" />
    <link rel="icon" type="image/png" sizes="48x48" href="{{ site_config.base_url }}/assets/favicon/favicon-48x48.png" />
    <link rel="apple-touch-icon" href="{{ site_config.base_url }}/assets/favicon/apple-touch-icon.png" />
    <link rel="icon" type="image/png" sizes="192x192" href="{{ site_config.base_url }}/assets/favicon/favicon-192x192.png" />
    <link rel="icon" type="image/png" sizes="512x512" href="{{ site_config.base_url }}/assets/favicon/favicon-512x512.png" />
    <!-- End favicon links -->
    <script src="https://polyfill.io/v3/polyfill.min.js?features=es6"></script>
    <script>
      window.MathJax = {
        tex: {
          inlineMath: [['$', '$'], ['\\(', '\\)']],
          displayMath: [['$$', '$$'], ['\\[', '\\]']],
          processEscapes: true
        },
        options: {
          ignoreHtmlClass: 'no-mathjax',
          processHtmlClass: 'mathjax'
        },
        startup: {
          pageReady: function() {
            return MathJax.startup.defaultPageReady().then(function() {
              // Force update math when the page loads
              MathJax.typeset();
            });
          }
        }
      };
    </script>
    <script
      id="MathJax-script"
      async
      src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"
    ></script>
  </head>
  <body>
    <header class="site-header">
      <div class="container">
        <a class="site-title" href="{{ site_config.base_url }}/"
          >{{ site_config.title }}</a
        >
        <nav class="site-nav">
          <a href="{{ site_config.base_url }}/">Home</a>
          <a href="{{ site_config.base_url }}/euler-library/">Euler Library</a>
          <a
            href="{{ site_config.github_repo }}"
            target="_blank"
            rel="noopener"
            >GitHub</a
          >
        </nav>
        <img class="site-logo" src="{{ site_config.base_url }}/assets/favicon/favicon-192x192.png" alt="Logo" />
      </div>
    </header>

    <main class="page-content">
      <div class="container">{% block content %}{% endblock %}</div>
    </main>

    <footer class="site-footer">
      <div class="container">
        <p>
          &copy; {{ current_year }} {{ site_config.author }}. Built with Python for
          Project Euler Solutions.
        </p>
      </div>
    </footer>
  </body>
</html>""")

    with open(TEMPLATES_DIR / "index.html", "w") as f:
        f.write("""{% extends "base.html" %}

{% block title %}Home | {{ site_config.title }}{% endblock %}

{% block content %}
<h1 id="project-euler-solutions">Project Euler Solutions by Geo Kim</h1>

<p>Hi! My name is Geo Kim. Welcome to my Project Euler solutions repository! This site showcases my journey through solving Project Euler problems using Python.</p>

<h2 id="what-is-project-euler">What is Project Euler?</h2>

<p><a href="https://projecteuler.net/">Project Euler</a> is a series of challenging mathematical/computer programming problems that require more than just mathematical insights to solve. Although mathematics will help you arrive at elegant and efficient methods, the use of a computer and programming skills will be required to solve most problems.</p>

<h2 id="problem-solutions">Problem Solutions</h2>

<p>Below is a list of all the problems I've solved so far:</p>

<div class="problem-table-container">
  <table class="problem-table">
    <thead>
      <tr>
        <th>Problem #</th>
        <th>Title</th>
      </tr>
    </thead>
    <tbody>
      {% for problem in problems %}
        <tr class="problem-row" data-href="{{ site_config.base_url }}/problems/problem-{{ problem.number }}/">
          <td class="problem-number">
            <a href="{{ site_config.base_url }}/problems/problem-{{ problem.number }}/">{{ problem.number }}</a>
          </td>
          <td class="problem-title">{{ problem.title }}</td>
        </tr>
      {% endfor %}
    </tbody>
  </table>
</div>

<script>
  document.addEventListener('DOMContentLoaded', function() {
    const rows = document.querySelectorAll('tr.problem-row');
    rows.forEach(row => {
      row.addEventListener('click', function() {
        window.location.href = this.dataset.href;
      });
    });
  });
</script>
{% endblock %}""")

    with open(TEMPLATES_DIR / "problem.html", "w") as f:
        f.write("""{% extends "base.html" %}

{% block title %}{{ problem.title }} | {{ site_config.title }}{% endblock %}

{% block content %}
<div class="problem-page">
  <div class="problem-navigation">
    <a href="{{ site_config.base_url }}/" class="home-link">← Home</a>
    <h1>Problem {{ problem.number }}: {{ problem.title }}</h1>
    <div class="nav-buttons">
      {% if prev_problem %}      
      <a
        href="{{ site_config.base_url }}/problems/problem-{{ prev_problem.number }}/"
        class="nav-button prev-button"
        >← Previous</a
      >
      {% endif %}
      
      {% if next_problem %}
      <a
        href="{{ site_config.base_url }}/problems/problem-{{ next_problem.number }}/"
        class="nav-button next-button"
        >Next →</a
      >
      {% endif %}
    </div>
  </div>

  <div class="problem-statement">
    <h2>Problem Statement</h2>
    <div class="statement-content mathjax">{{ problem.statement | safe }}</div>
  </div>

  <div class="problem-solution">
    <h2>Solution</h2>
    <div class="code-container">
      {{ highlighted_code | safe }}
    </div>
  </div>
</div>
{% endblock %}""")

    with open(TEMPLATES_DIR / "euler_library.html", "w") as f:
        f.write("""{% extends "base.html" %}

{% block title %}Euler Library | {{ site_config.title }}{% endblock %}

{% block content %}
<h1>Euler Helper Library</h1>

<p>This is a collection of utility functions used across multiple Project Euler problem solutions.</p>

<div class="euler-library">
  {% for function in euler_functions %}
  <div class="euler-function">
    <h3>{{ function.name }}</h3>
    <div class="function-description">
      <p>{{ function.description }}</p>
    </div>
    <div class="code-container">
      {{ function.code | safe }}
    </div>
  </div>
  {% endfor %}
</div>
{% endblock %}""")

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
