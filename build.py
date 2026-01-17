import os
import glob
import json
import re
import frontmatter
import markdown
from jinja2 import Environment, FileSystemLoader
from datetime import datetime

# Configuration
CONTENT_DIR = "content/posts"
OUTPUT_DIR = "blog_posts"
TEMPLATE_DIR = "templates"
ASSETS_JS_DIR = "assets/js"


def format_date(date_obj):
    if isinstance(date_obj, str):
        # Try parsing YYYY-MM-DD
        try:
            date_obj = datetime.strptime(date_obj, "%Y-%m-%d")
        except ValueError:
            return date_obj  # Return as is if format unknown
    return date_obj.strftime("%B %-d, %Y")


def main():
    # Setup Jinja2
    env = Environment(loader=FileSystemLoader(TEMPLATE_DIR))
    template = env.get_template("post.html")

    posts_metadata = []

    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    if not os.path.exists(ASSETS_JS_DIR):
        os.makedirs(ASSETS_JS_DIR)

    # Process each markdown file
    for md_file in glob.glob(os.path.join(CONTENT_DIR, "*.md")):
        print(f"Processing {md_file}...")
        # Load post
        post = frontmatter.load(md_file)

        basename = os.path.basename(md_file)
        html_filename = os.path.splitext(basename)[0] + ".html"

        # Extract metadata
        metadata = post.metadata
        content = markdown.markdown(
            post.content, extensions=["fenced_code", "codehilite", "tables"]
        )

        # Transform local markdown links to html links
        # This handles [Text](post.md) -> <a href="post.html">Text</a>
        content = re.sub(r'href="([^"]+)\.md"', r'href="\1.html"', content)

        # Prepare context for template
        date_obj = metadata.get("date")
        date_str = str(date_obj)  # Keep YYYY-MM-DD for datetime attribute
        date_display = format_date(date_obj)

        context = {
            "title": metadata.get("title"),
            "date": date_str,
            "date_display": date_display,
            "tags": metadata.get("tags", []),
            "excerpt": metadata.get("excerpt", ""),
            "content": content,
            "extra_head": metadata.get("extra_head", ""),
            "extra_scripts": metadata.get("extra_scripts", ""),
        }

        # Render HTML
        html_output = template.render(context)

        # Write HTML file
        output_path = os.path.join(OUTPUT_DIR, html_filename)
        with open(output_path, "w") as f:
            f.write(html_output)

        print(f"  Generated {html_filename}")

        # Add to metadata list
        posts_metadata.append(
            {
                "title": metadata.get("title"),
                "date": date_str,
                "url": f"blog_posts/{html_filename}",
                "excerpt": metadata.get("excerpt", ""),
                "tags": metadata.get("tags", []),
            }
        )

    # Sort posts by date (newest first)
    posts_metadata.sort(key=lambda x: x["date"], reverse=True)

    # Generate blog_data.js
    js_content = f"window.blogPosts = {json.dumps(posts_metadata, indent=2)};"
    with open(os.path.join(ASSETS_JS_DIR, "blog_data.js"), "w") as f:
        f.write(js_content)

    print(f"Generated blog_data.js with {len(posts_metadata)} posts")


if __name__ == "__main__":
    main()
