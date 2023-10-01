import click
import re
import shutil
from pathlib import Path
import subprocess as sub
import platform
import fileinput
import configparser


@click.command()
@click.option("--file_path", type=str, default=None)
def main(file_path: str):
    file = Path(file_path)
    if file.is_file():
        config = configparser.ConfigParser()
        config.read("config.ini")

        file_name = file.stem

        if file.suffix == ".md":
            # Copy the article as is
            shutil.copy(file_path, f"{config['Path']['articles']}/{file_name}.md")

            # Write the brief
            with open(
                f"{config['Path']['briefs']}/{file_name}.md", "w", encoding="utf-8"
            ) as f:
                f.write(get_first_400_characters(file))
                f.write("...\n")

        elif file.suffix == ".ipynb":
            if platform.system() == "Windows":
                python = "py"
            elif platform.system() == "Linux":
                python = "python3"

            # Run black on the notebook
            print(" - Running black on {file}")
            sub.run([python, "-m", "black", file])

            # Retarget file to the temporary (Markdown) one
            file = Path(f"{config['Path']['raws']}/tmp/{file_name}.md")

            # Prepare the temporary markdown file
            sub.run(
                [
                    python,
                    "-m",
                    "nbconvert",
                    "--to",
                    "markdown",
                    f"--output-dir={config['Path']['raws']}/tmp",
                    f"{config['Path']['raws']}/{file_name}.ipynb",
                ]
            )

            # Copy the article as is
            shutil.copy(file, f"{config['Path']['articles']}/{file_name}.md")

            # Write the brief
            with open(
                f"{config['Path']['briefs']}/{file_name}.md", "w", encoding="utf-8"
            ) as f:
                f.write(get_first_400_characters(file))
                f.write("...\n")

            # Erase the previously generated figures
            remove_files_with_pattern(config["Path"]["media"], f"{file_name}_*.png")

            # Copy all temporary figures to the media directory
            png_files = Path(f"{config['Path']['raws']}/tmp/{file_name}_files").glob(
                "*.png"
            )
            for f in png_files:
                shutil.copy(f, Path(config["Path"]["media"]))

            # Delete the temporary files
            shutil.rmtree(f"{config['Path']['raws']}/tmp")

            # Update the temporary media links
            retarget_temporary_media_files(
                Path(f"{config['Path']['articles']}/{file_name}.md")
            )

        # Copy all non-temporary figures to the media directory
        png_files = Path(f"{config['Path']['raws']}/media").glob(f"{file_name}_*.png")
        for f in png_files:
            shutil.copy(f, Path(config["Path"]["media"]))

        # Update the non-temporary media links
        retarget_non_temporary_media_files(
            Path(f"{config['Path']['articles']}/{file_name}.md")
        )

        latex_to_image(Path(f"{config['Path']['articles']}/{file_name}.md"), config)


def remove_files_with_pattern(directory_path, pattern):
    directory = Path(directory_path)
    for file in directory.glob(pattern):
        file.unlink()


def retarget_temporary_media_files(path: Path):
    print(f" - Retargetting temporary media files for {path}")
    with fileinput.FileInput(path, inplace=True) as file:
        for line in file:
            # Nbconvert generates images with ![png](<path>)
            print(
                line.replace(
                    f"![png]({path.stem}_files/",
                    "![png](../media/",
                ),
                end="",
            )


def retarget_non_temporary_media_files(path: Path):
    print(f" - Retargetting non-temporary media files for {path}")
    with fileinput.FileInput(path, inplace=True) as file:
        for line in file:
            if "![png](" in line:
                print(
                    line.replace(
                        f"![png](media/",
                        "![png](../media/",
                    ),
                    end="",
                )
            elif "![img](" in line:
                print(
                    line.replace(
                        f"![img](media/",
                        "![img](../media/",
                    ),
                    end="",
                )
            else:
                print(
                    line,
                    end="",
                )


def get_first_400_characters(file: Path) -> str:
    content = file.read_text()

    # Remove hyperlinks
    content = re.sub(r"\[(.*?)\]\((.*?)\)", r"\1", content)

    # Get the first 400 characters (approximately)
    first_400_characters = content[:400]

    return first_400_characters


def replace_matches(
    match: re.match, counter: int, filename: str, config: configparser.ConfigParser
) -> str:
    tex = match.strip("%%latex\n$")
    print(f' - LaTeX string "{tex}" to be replaced with an image.')

    # Image filename
    img_filename = f"{filename}_latex_{counter:02d}"

    # Generate the image of the LaTeX expression
    sub.run(
        [
            "bash",
            "./tex2png.sh",
            tex,
            img_filename,
        ]
    )

    # Move the image to the correct location
    Path(f"{config['Path']['media']}/{img_filename}.png").unlink(missing_ok=True)
    shutil.move(f"tmp/{img_filename}.png", config["Path"]["media"])

    # Change the LaTeX with the image reference for the Markdown file
    replacement = f"\n\n\n![png](../media/{img_filename}.png)\n\n\n"

    print(f' - LaTeX string "{tex}" replaced with "{replacement}"')
    return replacement


def latex_to_image(file: Path, config: configparser.ConfigParser):
    print(f" - Converting LaTeX to images for file {file}")

    content = file.read_text()

    pattern = r"%%latex\n\$([^$]+)\$"

    matches = re.findall(pattern, content, flags=re.DOTALL)

    counter = 0
    for match in matches:
        replacement = replace_matches(match, counter, file.stem, config)
        print(f' - Replacing "%%latex\n${match}$" with {replacement}')
        content = content.replace(f"%%latex\n${match}$", replacement, 1)
        counter += 1

    file.write_text(content)


if __name__ == "__main__":
    main()
