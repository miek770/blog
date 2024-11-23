# My personal blog

This is the code for my personnal blog, see this first article and guide for details: [https://codecurrents.blog/article/2023-07-06](https://codecurrents.blog/article/2023-07-06).

## Usage

New articles, written either as [Markdown](https://www.markdownguide.org/) files (\*.md) or [Jupyter Notebooks](https://jupyter.org/) (\*.ipynb), must be created in the `raws` directory. Their filename must be a date in ISO format (i.e.: `YYYY-MM-DD`), followed by the extension (e.g.: `2023-09-16.ipynb`).

PNG images can be included in the `raws/media` subdirectory; they need to start with the relevant article's date, followed by `.png` (e.g.: `2023-09-16_Figure1.png`). Their [Markdown](https://www.markdownguide.org/) line must use `png` or `img` as their alternative title, e.g.: `![png]( <image.ext> )`.

Raw articles can be processed with `make publish`; only raws that have changed since the last execution of `make publish` will be processed. This process converts Notebooks to Markdown, converts LaTeX to images, extracts briefs, and retargets media files. The output is saved under `web/articles`, `web/briefs` and `web/media`.

`make publish` also updates the RSS feed, under `web/static/rss.xml`.

The website can be launched with `make serve` during development (for testing). On my server, I use a systemd service file with the following content:

```ini
[Unit]
Description=Blog
After=network.target

[Service]
User=michel
WorkingDirectory=/home/michel/blog
ExecStart=/home/michel/.pyenv/shims/poetry run python /home/michel/blog/web/main.py
Restart=on-failure

[Install]
WantedBy=multi-user.target
```

## Updates

The repo has changed somewhat since its creation. Its dependencies are now managed with `poetry` and the Python version with `pyenv`. Both were installed through my package manager (`pacman`) but instructions vary per operating system.

### LaTeX

`pdflatex` is needed during the conversion of raw articles. On Arch linux I needed to install the following libraries to make it work (they might not all be required, but I hate debugging LaTeX and would rather install too many than to few):

```bash
sudo pacman -S texlive-binextra texlive-latex texlive-latexextra texlive-plaingeneric texlive-mathscience
```
### Proofreading

I have disabled the [proofreading using ChatGPT](https://codecurrents.blog/article/2023-07-16) feature.