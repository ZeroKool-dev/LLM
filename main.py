import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types

def main():
    # Ensure a prompt was provided
    if len(sys.argv) < 2:
        print("Error: Please provide a prompt as a command line argument.")
        print("Example: uv run main.py \"Why is backend development fun?\"")
        sys.exit(1)

    # Read user prompt from CLI
    user_prompt = sys.argv[1]

    # Track user prompt
    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]

    # Load environment variables
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")

    # Create Gemini client
    client = genai.Client(api_key=api_key)

    # Generate content
    response = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=messages
    )

    # Print response text
    print(response.text)

    # Token usage
    prompt_tokens = response.usage_metadata.prompt_token_count
    response_tokens = response.usage_metadata.candidates_token_count

    print(f"Prompt tokens: {prompt_tokens}")
    print(f"Response tokens: {response_tokens}")

if __name__ == "__main__":
    main()
