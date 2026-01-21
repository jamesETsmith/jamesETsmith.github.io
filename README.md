# James E. T. Smith's Website

This repository contains the source code and content for my personal website and blog, hosted on GitHub Pages.

## Project Structure

- `content/posts/`: Markdown source files for blog posts
- `templates/`: HTML templates (Jinja2)
- `assets/`: Static assets (CSS, JS)
- `images/`: Images used in the blog and website
- `build.py`: Python script to generate the static HTML files
- `build/`: Output directory (not committed)
- `*.html`: Generated static HTML files (in root for GitHub Pages)

## Building the Site

To build the static site from the markdown content:

1. Ensure you have the required dependencies:
   ```bash
   pip install -r requires.txt
   ```
   (Note: `requires.txt` is inside `jamesetsmith_github_io.egg-info/`, you might need to create a `requirements.txt` or install manually: `jinja2`, `markdown`, `python-frontmatter`)

2. Run the build script:
   ```bash
   python build.py
   ```

3. The script will:
   - Process markdown files in `content/posts/`
   - Apply templates from `templates/`
   - Generate HTML files in `blog_posts/`
   - Update `assets/js/blog_data.js` for the blog index

## Writing Blog Posts

Create a new `.md` file in `content/posts/` with the following frontmatter:

```yaml
---
title: Your Post Title
date: YYYY-MM-DD
tags: [tag1, tag2]
excerpt: A short summary of the post.
---

Your content here...
```

### Math Support
The blog supports LaTeX-style math rendering via MathJax.
- **Inline Math**: Use single dollar signs `$ E = mc^2 $`
- **Block Math**: Use double dollar signs `$$ E = mc^2 $$`
- **Numbered Equations**: Use the `equation` environment inside block math delimiters:
  ```latex
  $$
  \begin{equation}
    y = mx + b \label{eq:line}
  \end{equation}
  $$
  ```

### Margin Notes (Admonitions)
You can add color-coded margin notes (which float to the right on desktop and appear inline on mobile) using the `admonition` syntax. Place the note **before** the paragraph you want it to align with.

**Theory Note (Green)**
```markdown
!!! theory "Title Optional"
    This is a theory note.
```

**Applied Note (Blue)**
```markdown
!!! applied "Title Optional"
    This is an applied note.
```

**Implementation Note (Orange)**
```markdown
!!! implementation "Title Optional"
    This is an implementation note.
```

**Key Points Note (Purple)**
```markdown
!!! key-points "Summary"
    This is a key points note.
```

## Theme

The site supports both light and dark modes. The preference is saved in `localStorage` or defaults to the system preference.
