#!/usr/bin/env python3
"""
Script to automatically extract metadata from blog post HTML files
and generate a JSON file with blog post information.
"""

import os
import re
import json
from pathlib import Path


def extract_date_from_filename(filename):
    """Extract date from filename in format YYYY_MM_DD.html"""
    match = re.match(r'(\d{4})_(\d{2})_(\d{2})\.html', filename)
    if match:
        year, month, day = match.groups()
        return f"{year}-{month}-{day}"
    return None


def parse_blog_post(file_path):
    """Parse a single blog post HTML file and extract metadata."""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    filename = os.path.basename(file_path)
    
    # Extract title from h2 in post-header
    title_match = re.search(r'<header\s+class=["\']post-header["\']>.*?<h2>([^<]+)</h2>', content, re.DOTALL)
    title = title_match.group(1).strip() if title_match else None
    
    # Extract date from filename first (most reliable)
    date = extract_date_from_filename(filename)
    
    # Fallback: extract date from time tag datetime attribute if filename doesn't have date
    if not date:
        date_match = re.search(r'<time\s+datetime=["\']([^"\']+)["\']', content)
        date = date_match.group(1) if date_match else None
    
    # Extract tags from span tags with class="tag"
    tags = []
    tag_matches = re.findall(r'<span\s+class=["\']tag["\']>([^<]+)</span>', content)
    tags.extend([tag.strip() for tag in tag_matches if tag.strip()])
    
    # Fallback: try to extract from meta keywords if tags not found
    if not tags:
        keywords_match = re.search(r'<meta\s+name=["\']keywords["\']\s+content=["\']([^"\']+)["\']', content)
        if keywords_match:
            tags = [tag.strip() for tag in keywords_match.group(1).split(',') if tag.strip()]
    
    # Extract excerpt from meta description (handle multiline attributes and apostrophes)
    # Match the description meta tag, handling multiline format
    # Need to match content="..." where ... can contain apostrophes
    # Use a pattern that matches until " followed by /> or >
    meta_desc_match = re.search(
        r'<meta\s+name=["\']description["\'][\s\S]*?content=(["\'])(.*?)\1',
        content,
        re.IGNORECASE
    )
    if meta_desc_match:
        excerpt = meta_desc_match.group(2).strip()
    else:
        excerpt = None
    
    # Generate excerpt from first paragraph if not in meta description
    if not excerpt:
        # Try to find first paragraph in post-section
        para_match = re.search(r'<section\s+class=["\']post-section["\']>.*?<p>([^<]+)</p>', content, re.DOTALL)
        if para_match:
            excerpt = para_match.group(1).strip()
            # Limit excerpt length
            if len(excerpt) > 200:
                excerpt = excerpt[:197] + "..."
    
    return {
        'title': title or 'Untitled',
        'date': date or '1970-01-01',
        'url': f"blog_posts/{filename}",
        'excerpt': excerpt or '',
        'tags': tags
    }


def main():
    """Main function to scan blog posts directory and generate metadata JSON."""
    blog_posts_dir = Path(__file__).parent / 'blog_posts'
    output_file = Path(__file__).parent / 'blog_metadata.json'
    
    if not blog_posts_dir.exists():
        print(f"Error: {blog_posts_dir} does not exist")
        return
    
    blog_posts = []
    
    # Find all HTML files in blog_posts directory
    for html_file in sorted(blog_posts_dir.glob('*.html'), reverse=True):
        print(f"Processing {html_file.name}...")
        try:
            post_data = parse_blog_post(html_file)
            blog_posts.append(post_data)
            print(f"  ✓ Title: {post_data['title']}")
            print(f"  ✓ Date: {post_data['date']}")
            print(f"  ✓ Tags: {', '.join(post_data['tags'])}")
            print(f"  ✓ Excerpt: {post_data['excerpt'][:50]}...")
        except Exception as e:
            print(f"  ✗ Error processing {html_file.name}: {e}")
    
    # Sort by date (newest first)
    blog_posts.sort(key=lambda x: x['date'], reverse=True)
    
    # Write JSON file
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(blog_posts, f, indent=2, ensure_ascii=False)
    
    print(f"\n✓ Generated {output_file} with {len(blog_posts)} blog posts")


if __name__ == '__main__':
    main()

