# My personal blog

This is the code for my personnal blog, see this first article and guide for details: [https://codecurrents.blog/article/2023-07-06](https://codecurrents.blog/article/2023-07-06).

## Update

The repo has changed somewhat since its creation. Its dependencies are now managed with `poetry` and the Python version with `pyenv`. Both were installed through my package manager (`pacman`) but instructions vary per operating system.

### LaTeX

`pdflatex` is needed during the conversion of raw articles. On Arch linux I needed to install the following libraries to make it work (they might not all be required, but I hate debugging LaTeX and would rather install too many than to few):

```bash
sudo pacman -S texlive-binextra texlive-latex texlive-latexextra texlive-plaingeneric texlive-mathscience
```
