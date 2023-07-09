import click
import re
import shutil
from pathlib import Path
import subprocess as sub
import platform


def get_first_400_characters(file: Path) -> str:
    content = file.read_text()

    # Remove hyperlinks
    content = re.sub(r'\[(.*?)\]\((.*?)\)', r'\1', content)

    # Get the first 400 characters (approximately)
    first_400_characters = content[:400]

    return first_400_characters


@click.command()
@click.option("--file_path", type=str, default=None)
def main(file_path: str):
    file = Path(file_path)
    if file.is_file():
        file_name = file.stem

        if file.suffix == ".md":
            # Copy the article as is
            shutil.copy(file_path, f"web/articles/{file_name}.md")

            # Write the brief
            with open(f"web/briefs/{file_name}.md", "w", encoding='utf-8') as f:
                f.write(get_first_400_characters(file))
                f.write("...")

        elif file.suffix == ".ipynb":
            if platform.system() == 'Windows':
                python = "py"
            elif platform.system() == 'Linux':
                python = "python3"

            # Generate the HTML article
            sub.run([
                python,
                "-m",
                "nbconvert",
                "--to",
                "html",
                "--output-dir=web/articles",
                f"raws/{file_name}.ipynb",
                ])

            # Prepare the temporary markdown file for the brief
            sub.run([
                python,
                "-m",
                "nbconvert",
                "--to",
                "markdown",
                "--output-dir=raws/tmp",
                f"raws/{file_name}.ipynb",
                ])

            # Write the brief
            file = Path(f"raws/tmp/{file_name}.md")
            with open(f"web/briefs/{file_name}.md", "w", encoding='utf-8') as f:
                f.write(get_first_400_characters(file))
                f.write("...")

            # Delete the temporary files
            shutil.rmtree("raws/tmp")


if __name__ == "__main__":
    main()
