import argparse
import os

from dotenv import load_dotenv
from google import genai
from google.genai import types

from call_function import available_functions, call_function
from prompts import system_prompt


def main():
    parser = argparse.ArgumentParser(description="AI Code Assistant")
    parser.add_argument("user_prompt", type=str, help="Prompt to send to Gemini")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY environment variable not set")

    client = genai.Client(api_key=api_key)
    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]
    if args.verbose:
        print(f"User prompt: {args.user_prompt}\n")

    generate_content(client, messages, args.verbose)


def generate_content(client, messages, verbose):
    max_iterations = 20
    for _ in range(max_iterations):
        try:
            response = client.models.generate_content(
                model="gemini-2.5-flash-lite",
                contents=messages,
                config=types.GenerateContentConfig(
                    tools=[available_functions], system_instruction=system_prompt
                ),
            )
        except Exception as e:
            print(f"Error during generate_content: {e}")
            return

        if not response.usage_metadata:
            raise RuntimeError("Gemini API response appears to be malformed")

        if verbose:
            print("Prompt tokens:", response.usage_metadata.prompt_token_count)
            print("Response tokens:", response.usage_metadata.candidates_token_count)

        if response.candidates:
            for candidate in response.candidates:
                if candidate.content:
                    messages.append(candidate.content)

        function_call_parts = []  # Captured tool responses for potential follow-up turns
        if response.function_calls:
            for function_call_part in response.function_calls:
                function_call_result = call_function(function_call_part, verbose=verbose)
                if (
                    not function_call_result.parts
                    or not function_call_result.parts[0].function_response
                    or function_call_result.parts[0].function_response.response is None
                ):
                    raise RuntimeError(
                        "Function response missing from call_function result"
                    )

                function_call_parts.append(function_call_result.parts[0])
                if verbose:
                    print(f"-> {function_call_result.parts[0].function_response.response}")

        if function_call_parts:
            messages.append(types.Content(role="user", parts=function_call_parts))

        candidates_have_function_call = any(
            any(
                getattr(part, "function_call", None) is not None
                for part in (candidate.content.parts or [])
            )
            for candidate in (response.candidates or [])
            if candidate.content and candidate.content.parts
        )
        is_finished = not candidates_have_function_call and bool(response.text)

        if is_finished:
            print("Response:")
            print(response.text)
            return

    print("Maximum iterations reached without completion.")


if __name__ == "__main__":
    main()
