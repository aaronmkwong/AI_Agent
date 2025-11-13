from google import genai               # Import the Google GenAI client package
import sys                             # System utilities (exit, argv, etc.)
import os                              # Environment variables and OS interactions
from dotenv import load_dotenv         # Load variables from a .env file into the environment
from google.genai import types         # Types for constructing message contents
import argparse                        # Parse command-line arguments
from functions.config import *         # Get variables
from functions.get_files_info import * # Get schema declaration to tell the LLM how to use the function

# Define positional prompt
parser = argparse.ArgumentParser()    # Create an argument parser for the CLI
parser.add_argument("prompt", type=str, help="User prompt")            # Required positional prompt string
parser.add_argument("--verbose", action="store_true", help="Enable verbose mode")  # Optional flag

def main():
    args = parser.parse_args()        # Parse CLI args into an object (args.prompt, args.verbose)

    load_dotenv()                     # Load .env file so GEMINI_API_KEY is available
    api_key = os.environ.get("GEMINI_API_KEY")  # Read the API key from environment
    if not api_key:                   # If missing, inform and exit
        print("Missing GEMINI_API_KEY")
        sys.exit(1)

    client = genai.Client(api_key=api_key)  # Initialize the GenAI client

    # Build the message list with the user prompt as a single user turn
    messages = [
        types.Content(role="user", parts=[types.Part(text=args.prompt)]),
    ]

    # Create a list of all the available functions for LLM to use
    available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_run_python_file,
        schema_write_file,
        ]
    )   

    # Send the request to the model with the conversation contents
    resp = client.models.generate_content(
        model=model_name,
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions], system_instruction=system_prompt
            ),

    )

    if args.verbose: # Checks if 'verbose' flag passed as a command-line argument
        print(f'User prompt: "{args.prompt}"')  

        # getattr() function tries to find attribute and if not found return default value instead of crashing program
        meta = getattr(resp, "usage_metadata", None) 
        prompt_tokens = getattr(meta, "prompt_token_count", "unknown") if meta else "unknown"
        resp_tokens = getattr(meta, "candidates_token_count", "unknown") if meta else "unknown"
        
        print(f"Prompt tokens: {prompt_tokens}")
        print(f"Response tokens: {resp_tokens}")

    # if function_calls (list of function-call parts) contains any items, iterate over them and print the function name and arguments else print the model's text response
    if len(resp.function_calls) > 0:
        for _ in resp.function_calls:
            print(f"Calling function: {_.name}({_.args})") 
    else:
        print(resp.text)                   

if __name__ == "__main__":             # Only run main when executed as a script
    main()