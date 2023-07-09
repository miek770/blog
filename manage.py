import click
import re
import shutil
from pathlib import Path
import subprocess as sub
import platform
import fileinput


def retarget_media_files(path: Path):
    # Open the file in place for editing
    with fileinput.FileInput(path, inplace=True) as file:
        # Iterate over each line in the file
        for line in file:
            # Replace the target string with the desired replacement
            updated_line = line.replace("![png](2023-07-xx_files/", "![png](../media/")
            # Print the modified line to the file
            print(updated_line, end='')


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

            # Retarget file to the temporary (Markdown) one
            file = Path(f"raws/tmp/{file_name}.md")

            # Prepare the temporary markdown file
            sub.run([
                python,
                "-m",
                "nbconvert",
                "--to",
                "markdown",
                "--output-dir=raws/tmp",
                f"raws/{file_name}.ipynb",
                ])

            # Copy the article as is
            shutil.copy(file, f"web/articles/{file_name}.md")

            # Write the brief
            with open(f"web/briefs/{file_name}.md", "w", encoding='utf-8') as f:
                f.write(get_first_400_characters(file))
                f.write("...")

            # Copy all figures to the media directory
            png_files = Path(f"raws/tmp/{file_name}_files").glob("*.png")
            for f in png_files:
                shutil.copy2(f, Path("web/media"))

            # Delete the temporary files
            shutil.rmtree("raws/tmp")

            # Update the media links
            retarget_media_files(Path(f"web/articles/{file_name}.md"))


if __name__ == "__main__":
    main()
