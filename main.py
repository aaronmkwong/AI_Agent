from google import genai              # Import the Google GenAI client package
import sys                            # System utilities (exit, argv, etc.)
import os                             # Environment variables and OS interactions
from dotenv import load_dotenv        # Load variables from a .env file into the environment
from google.genai import types        # Types for constructing message contents
import argparse                       # Parse command-line arguments
from functions.config import *        # Get variables

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

    # Send the request to the model with the conversation contents
    resp = client.models.generate_content(
        model=model_name,
        contents=messages,
        config=types.GenerateContentConfig(system_instruction=system_prompt),

    )

    if args.verbose: # Checks if 'verbose' flag passed as a command-line argument
        print(f'User prompt: "{args.prompt}"')  

        # getattr() function tries to find attribute and if not found return default value instead of crashing program
        meta = getattr(resp, "usage_metadata", None) 
        prompt_tokens = getattr(meta, "prompt_token_count", "unknown") if meta else "unknown"
        resp_tokens = getattr(meta, "candidates_token_count", "unknown") if meta else "unknown"
        
        print(f"Prompt tokens: {prompt_tokens}")
        print(f"Response tokens: {resp_tokens}")

    print(resp.text)                   # Print the model’s text response

if __name__ == "__main__":             # Only run main when executed as a script
    main()