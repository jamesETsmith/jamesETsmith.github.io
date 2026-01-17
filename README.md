# Personal Website

Serve locally with:

```shell
python3 -m http.server 8888
```

## Blogging

### Adding a New Post

1.  Create a new Markdown file in `content/posts/` (e.g., `content/posts/YYYY-MM-DD-my-new-post.md`).
2.  Add the required front matter at the top of the file:

    ```yaml
    ---
    title: My New Post Title
    date: YYYY-MM-DD
    tags: [tag1, tag2]
    excerpt: A brief summary of the post.
    ---
    
    Your content goes here...
    ```

### Building the Blog

Run the build script to generate the HTML files and update the metadata:

```shell
# Assuming you have the virtual environment set up
.venv/bin/python build.py
```

To set up the environment for the first time:

```shell
uv venv
uv pip install .
```
