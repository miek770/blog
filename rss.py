import configparser
from pathlib import Path
from datetime import datetime
import pytz

# For the RSS feed generation
# https://feedgen.kiesow.be/
from feedgen.feed import FeedGenerator


def main():
    config = configparser.ConfigParser()
    config.read("config.ini")

    fg = FeedGenerator()
    fg.id("https://codecurrents.blog")
    fg.title("Code & Currents")
    fg.author({"name": "Michel Lavoie", "email": "lavoie.michel@gmail.com"})
    fg.link(href="https://codecurrents.blog", rel="alternate")
    fg.subtitle("Michel Lavoie's blog")
    fg.link(href="https://codecurrents.blog/feed", rel="self")
    fg.language("en")

    briefs = Path(config["Path"]["briefs"]).glob("*.md")
    for brief in briefs:
        pub_date = brief.stem
        with open(brief, "r") as file:
            for line in file:
                if line[:2] == "# ":
                    title = line[2:-1]
                    break

        with open(brief, "r") as file:
            for line in file:
                if line[0] == "*" and line[-2] == "*":
                    description = line[1:-2]
                    break

        id = f"{config['Site']['url']}/article/{pub_date}"

        fe = fg.add_entry()
        fe.id(id)
        fe.title(title)
        fe.link(href=id)
        fe.description(description)
        fe.author({"name": config["Site"]["author"], "email": config["Site"]["email"]})
        fe.content(f'{description}<br /><br />See full article at <a href="{id}">{id}</a>')

        date = datetime.strptime(pub_date, "%Y-%m-%d")
        timezone = pytz.timezone(config["Site"]["timezone"])
        date_with_timezone = timezone.localize(date)
        fe.pubDate(date_with_timezone)

    fg.rss_file(f"{config['Path']['static']}/rss.xml", pretty=True)


if __name__ == "__main__":
    main()
