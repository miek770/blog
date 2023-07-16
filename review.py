import openai
import click
from pathlib import Path


@click.command()
@click.argument("file_path", type=str)
def main(file_path: str):
    file = Path(file_path)
    if file.is_file():
        openai.api_key = Path("openai_api_key.txt").read_text()
        system_role = "You are a proofreader for my personal blog posts."
        model = "gpt-3.5-turbo-16k"
        request = f"""Look for grammatical errors in the following blog post.
Clearly highlight the errors in your response. Don't return the whole blog
post; limit your response to the errors and their context:\n\n
{file.read_text()}"""

        messages = [
            {
                "role": "system",
                "content": system_role,
            },
            {
                "role": "user",
                "content": request,
            },
        ]

        chat = openai.ChatCompletion.create(model=model, messages=messages)

        reply = chat.choices[0].message.content
        status = chat.choices[0].finish_reason

        print(f"Proofreading ({status}): {reply}")


if __name__ == "__main__":
    main()
