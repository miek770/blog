import datetime
from nicegui import ui
from pathlib import Path


__title__ = "Code & Currents - Michel Lavoie's blog"


briefs_dir = Path("web/briefs")
briefs_list = sorted(list(briefs_dir.glob("*")), reverse=True)

articles_dir = Path("web/articles")
articles_list = sorted(list(articles_dir.glob("*")), reverse=True)

body_classes = "mx-auto px-4 max-w-screen-md sm:max-w-full"


def briefs():
    for brief_path in briefs_list:
        if brief_path.is_file():
            # Show the card brief
            x = brief_path
            with ui.card().classes("container mx-auto").on(
                "click", lambda x=x: ui.open(f"/article/{x.stem}")
            ):
                with ui.row():
                    if brief_path.suffix == ".md":
                        ui.markdown(brief_path.read_text()).style("color: #555555")
                    elif brief_path.suffix == ".html":
                        ui.html(brief_path.read_text()).style("color: #555555")
                with ui.row().style("width: 100%").classes("flex justify-end"):
                    ui.link("Read article", f"/article/{brief_path.stem}")
                    ui.label(f"Posted on {brief_path.stem}")


def header():
    with ui.header().style("background-color: #F0F0F0").classes(
        "items-center place-content-center"
    ):
        ui.label(__title__).style("color: #111111")
        ui.link("Home", "/")
        ui.link("About", "/about")
        # ui.label("Search").style("color: #111111")
        # ui.input().props("dense")


def copyright():
    year = datetime.datetime.now().year
    with ui.expansion(f"Copyright © {year} Michel Lavoie. All rights reserved.").style(
        "color: #555555"
    ):
        ui.label(
            "Unauthorized use and/or duplication of this material without express and \
written permission from this blog's author and/or owner is strictly prohibited. \
Excerpts and links may be used, provided that full and clear credit is given to \
Michel Lavoie and [Your Blog's Name] with appropriate and specific direction to the \
original content."
        )


@ui.page("/")
def home():
    header()
    with ui.grid(columns=1).style("width: 100%").classes("place-items-center"):
        with ui.grid(columns=1).classes(body_classes):
            briefs()
            copyright()


@ui.page("/about")
def about():
    header()
    with ui.grid(columns=1).style("width: 100%").classes("place-items-center"):
        with ui.grid(columns=1).classes(body_classes):
            ui.markdown(Path("web/about.md").read_text())
            copyright()


@ui.page("/article/{date}")
def view_article(date: str):
    header()
    with ui.grid(columns=1).style("width: 100%").classes("place-items-center"):
        with ui.grid(columns=1).classes(body_classes):
            for article_path in articles_list:
                if date in article_path.stem:
                    if article_path.suffix == ".md":
                        ui.markdown(article_path.read_text())
                    elif article_path.suffix == ".html":
                        ui.html(article_path.read_text())
                    break
            copyright()


if __name__ in {"__main__", "__mp_main__"}:
    ui.run(title=__title__)

