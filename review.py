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

        messages = [
            {
                "role": "assistant",
                "content": system_role,
            },
            {
                "role": "user",
                "content": f"Review the following blog post:\n\n{file.read_text()}",
            },
        ]

        chat = openai.ChatCompletion.create(
            model=model, messages=messages
        )
        reply = chat.choices[-1].message.content
        status = chat.choices[-1].finish_reason

        print(f"Feedback ({status}): {reply}\n\n---\n")

        messages = [
            {
                "role": "assistant",
                "content": system_role,
            },
            {
                "role": "user",
                "content": f"Look for grammatical errors in the following blog post:\n\n{file.read_text()}",
            },
        ]

        chat = openai.ChatCompletion.create(
            model=model, messages=messages
        )
        reply = chat.choices[-1].message.content
        status = chat.choices[-1].finish_reason

        print(f"Proofreading ({status}): {reply}")


if __name__ == "__main__":
	main()