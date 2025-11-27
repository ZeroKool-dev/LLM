import argparse
import os
from dotenv import load_dotenv
from google import genai
from google.genai import types


def main():
    load_dotenv()

    parser = argparse.ArgumentParser(
        description="Send a prompt to Gemini and print the response."
    )
    parser.add_argument("prompt", help="The user prompt to send to Gemini.")
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Print debugging details like prompt and token counts.",
    )
    args = parser.parse_args()

    user_prompt = args.prompt

    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]

    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")

    client = genai.Client(api_key=api_key)

    response = client.models.generate_content(
        model="gemini-2.0-flash-001", contents=messages
    )

    print(response.text)

    if args.verbose:
        print(f"User prompt: {user_prompt}")
        prompt_tokens = response.usage_metadata.prompt_token_count
        response_tokens = response.usage_metadata.candidates_token_count
        print(f"Prompt tokens: {prompt_tokens}")
        print(f"Response tokens: {response_tokens}")


if __name__ == "__main__":
    main()
