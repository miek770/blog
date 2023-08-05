import datetime
from nicegui import app, ui
from pathlib import Path
import configparser
import dataset


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

media_dir = Path(config["Path"]["media"])
body_classes = "mx-auto sm:max-w-full"
body_style = "max-width: 768px;"


@ui.page("/")
def home():
    log_visit("/")
    header()
    with ui.grid(columns=1).classes(body_classes).style(body_style):
        briefs()
        footer()
        copyright()


@ui.page("/about")
def about():
    log_visit("/about")
    header()
    with ui.grid(columns=1).classes(body_classes).style(body_style):
        ui.markdown(Path(f"{config['Path']['static']}/about.md").read_text())
        footer()
        copyright()


@ui.page("/article/{date}")
def view_article(date: str):
    log_visit(f"/article/{date}")
    header(date)

    # Custom formatting
    ui.add_head_html(
        """
        <style>
            .nicegui-markdown pre {
                background-color: #f5f5f5;
                overflow: scroll;
            }
        </style>
    """
    )

    with ui.grid(columns=1).classes(body_classes).style(body_style):
        for article_path in articles_list:
            if date in article_path.stem:
                if article_path.suffix == ".md":
                    render_markdown_article(article_path)
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


def render_markdown_article(path: Path):
    if path.is_file():

        def get_target(line: str) -> str:
            return line.split("# ")[1].replace(" ", "_").replace("'", "_").lower()[:-1]

        # Find the link targets for the table of content
        targets = []
        in_code_block = False
        for line in path.open():
            if line.startswith("```"):
                in_code_block = not in_code_block
            if not in_code_block and line[0] == "#":
                target = get_target(line)
                targets.append((target, line))

        # Generate the table of content
        toc = []
        toc.append("## Content")
        for target, line in targets:
            title = line.split("# ")[1]
            link = f"[{title}](#{target})"

            # The levels start at zero for simplicity
            level = len(line.split("# ")[0])
            toc.append("   " * (level) + " - " + link)
        ui.markdown("\n".join(toc))

        # Print the article, including the link targets
        md = []
        in_code_block = False
        for line in path.open():
            if line.startswith("```"):
                in_code_block = not in_code_block
            if not in_code_block and line[0] == "#":
                ui.markdown("".join(md) + f'<a name="{get_target(line)}" />')
                md = []
            md.append(line)
        else:
            ui.markdown("".join(md))


def briefs():
    for brief_path in briefs_list:
        if brief_path.is_file():
            # Show the card brief
            x = brief_path
            with ui.card().classes("container mx-auto").on(
                "click",
                lambda x=x: ui.open(f"/article/{x.stem}"),
            ):
                if Path(media_dir, x.stem + ".png").is_file():
                    with ui.row().style("width: 100%").classes("place-content-center"):
                        ui.image(f"media/{x.stem}.png")
                with ui.row():
                    ui.markdown(brief_path.read_text()).style("color: #555555")
                with ui.row().style("width: 100%").classes("flex justify-end"):
                    ui.link("Read article", f"/article/{brief_path.stem}")
                    ui.label(f"Posted on {brief_path.stem}")


def header(date: str = None):
    # Google Search Console - Domain ownership verification
    ui.add_head_html(
        '<meta name="google-site-verification" content="xi7cLV-1mZiR8aMFkTLu4uWV8KdkK3D3lZURe_Luyy4" />'
    )

    # Offset anchors - Could be obsolete with:
    # https://github.com/zauberzeug/nicegui/pull/1329
    ui.add_head_html(
        """<style type="text/css">
            html {
                scroll-padding-top: 70px;
            }
        </style>
        """
    )

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
            ui.link("Back to top", "#")


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


def log_visit(path: str):
    with dataset.connect(config["Db"]["url"]) as db:
        db["visits"].insert(
            {
                "page": path,
                "datetime": datetime.datetime.now(),
            }
        )


if __name__ in {"__main__", "__mp_main__"}:
    app.add_media_files("/media", config["Path"]["media"])
    app.add_static_files("/static", config["Path"]["static"])
    ui.run(
        title=__title__,
        favicon="🐍",
    )
