import datetime
from nicegui import app, ui
from pathlib import Path
import configparser


config = configparser.ConfigParser()
config.read("config.ini")

__title__ = config["Site"]["title"] + " - " + config["Site"]["subtitle"]

__copyright__ = f"Unauthorized use and/or duplication of this material without \
express and written permission from this blog's author and/or owner is strictly \
prohibited. Excerpts and links may be used, provided that full and clear credit \
is given to {config['Site']['author']} and {config['Site']['title']} with \
appropriate and specific direction to the original content."


briefs_dir = Path(config["Path"]["briefs"])
briefs_list = sorted(list(briefs_dir.glob("*")), reverse=True)

articles_dir = Path(config["Path"]["articles"])
articles_list = sorted(list(articles_dir.glob("*")), reverse=True)

body_classes = "mx-auto sm:max-w-full"
body_style = "max-width: 768px;"


def briefs():
    for brief_path in briefs_list:
        if brief_path.is_file():
            # Show the card brief
            x = brief_path
            with ui.card().classes("container mx-auto").on(
                "click",
                lambda x=x: ui.open(f"/article/{x.stem}"),
            ):
                with ui.row():
                    ui.markdown(brief_path.read_text()).style("color: #555555")
                with ui.row().style("width: 100%").classes("flex justify-end"):
                    ui.link("Read article", f"/article/{brief_path.stem}")
                    ui.label(f"Posted on {brief_path.stem}")


def header(date: str = None):
    with ui.header().style("background-color: #F0F0F0").classes(
        "items-center place-content-center"
    ):
        ui.label(__title__).style("color: #111111")
        ui.link("Home", "/")
        ui.link("About", "/about")
        ui.link("RSS", "/feed")
        if date is not None:
            ui.link(
                "Source",
                f"{config['Site']['source']}/{config['Path']['articles']}/{date}.md",
            )


def copyright():
    year = datetime.datetime.now().year
    with ui.expansion(
        f"Copyright © {year} {config['Site']['author']}. All rights reserved."
    ).style("color: #555555"):
        ui.label(__copyright__)


def footer():
    ui.markdown(Path(f"{config['Path']['static']}/contact.md").read_text())

    credit = Path(f'{config["Path"]["static"]}/credit.md').read_text()
    ui.markdown(f"<small>{credit}</small>")


@ui.page("/")
def home():
    header()
    with ui.grid(columns=1).classes(body_classes).style(body_style):
        briefs()
        footer()
        copyright()


@ui.page("/about")
def about():
    header()
    with ui.grid(columns=1).classes(body_classes).style(body_style):
        ui.markdown(Path(f"{config['Path']['static']}/about.md").read_text())
        footer()
        copyright()


@ui.page("/article/{date}")
def view_article(date: str):
    header(date)

    # Custom formatting
    ui.add_head_html("""
        <style>
            .nicegui-markdown pre {
                background-color: #f5f5f5;
                overflow: scroll;
            }
        </style>
    """)

    with ui.grid(columns=1).classes(body_classes).style(body_style):
        for article_path in articles_list:
            if date in article_path.stem:
                if article_path.suffix == ".md":
                    ui.markdown(article_path.read_text())
                elif article_path.suffix == ".html":
                    ui.html(article_path.read_text())
                ui.html("<hr />")
                ui.link(
                    f"See source on {config['Site']['source_host']}",
                    f"{config['Site']['source']}/{config['Path']['articles']}/{date}.md",
                    )
                break
        footer()
        copyright()


# Only serves during debugging / testing
# Nginx serves this file in production
@ui.page("/feed")
def rss_feed():
    with open(f"{config['Path']['static']}/rss.xml", "r") as file:
        for line in file:
            ui.label(line)


# Only serves during debugging / testing
# Nginx serves this file in production
@ui.page("/robots.txt")
def rss_feed():
    with open(f"{config['Path']['static']}/robots.txt", "r") as file:
        for line in file:
            ui.label(line)


if __name__ in {"__main__", "__mp_main__"}:
    app.add_media_files("/media", config["Path"]["media"])
    app.add_static_files("/static", config["Path"]["static"])
    ui.run(title=__title__)
