import click
import re
import shutil


def get_first_400_characters(file_path: str) -> str:
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    # Remove Markdown hyperlinks
    content_without_links = re.sub(r'\[(.*?)\]\((.*?)\)', r'\1', content)

    # Get the first 400 characters (approximately)
    first_400_characters = content_without_links[:400]

    return first_400_characters


@click.command()
@click.option("--file_path", type=str, default=None)
def main(file_path: str):
    if file_path is not None:
        file_name = file_path.split("/")[1]
        with open(f"web/briefs/{file_name}", "w", encoding='utf-8') as file:
            file.write(get_first_400_characters(file_path))
            file.write("...")

        shutil.copy(file_path, f"web/articles/{file_name}")


if __name__ == "__main__":
    main()
