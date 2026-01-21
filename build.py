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
        
        # Pre-process content to protect math blocks from markdown parsing
        # We replace $$...$$ with a placeholder
        math_blocks = {}
        
        def replace_math_block(match):
            block_id = f"MATHBLOCK_{len(math_blocks)}"
            math_blocks[block_id] = match.group(0)
            return block_id

        # Protect block math $$...$$
        # Using [\\s\\S] to match newlines as well
        content = re.sub(r'\$\$[\s\S]*?\$\$', replace_math_block, post.content)
        
        # Protect inline math $...$
        # Negative lookbehind/lookahead to avoid matching $$
        content = re.sub(r'(?<!\$)\$(?!\$)[\s\S]*?(?<!\$)\$(?!\$)', replace_math_block, content)

        content = markdown.markdown(
            content, extensions=["fenced_code", "codehilite", "tables", "admonition"]
        )

        # Restore math blocks
        for block_id, math_code in math_blocks.items():
            content = content.replace(block_id, math_code)

        # Transform local markdown links to html links
        # This handles [Text](post.md) -> <a href="post.html">Text</a>
        content = re.sub(r'href="([^"]+)\.md"', r'href="\1.html"', content)

        # Check for admonitions to conditionally styling
        has_margin_notes = 'class="admonition' in content

        # Prepare context for template
        date_obj = metadata.get("date")
        date_str = str(date_obj)  # Keep YYYY-MM-DD for datetime attribute
        date_display = format_date(date_obj)
        is_draft = metadata.get("draft", False)

        context = {
            "title": metadata.get("title"),
            "date": date_str,
            "date_display": date_display,
            "tags": metadata.get("tags", []),
            "excerpt": metadata.get("excerpt", ""),
            "content": content,
            "extra_head": metadata.get("extra_head", ""),
            "extra_scripts": metadata.get("extra_scripts", ""),
            "has_margin_notes": has_margin_notes,
            "is_draft": is_draft,
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
                "is_draft": is_draft,
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
