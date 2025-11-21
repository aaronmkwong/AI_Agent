import sys                             # System utilities (exit, argv, etc.)
import os                              # Environment variables and OS interactions
from google import genai               # Import the Google GenAI client package
from google.genai import types         # Types for constructing message contents
from dotenv import load_dotenv         # Load variables from a .env file into the environment
import argparse                        # Parse command-line arguments

from functions.prompts import system_prompt
from functions.config import MAX_ITERS, model_name
from functions.call_function import call_function
from functions.get_files_info import schema_get_files_info, schema_get_file_content, schema_run_python_file, schema_write_file

# Define positional prompt
parser = argparse.ArgumentParser()    # Create an argument parser for the CLI
parser.add_argument("prompt", type=str, help="User prompt")            # Required positional prompt string
parser.add_argument("--verbose", action="store_true", help="Enable verbose mode")  # Optional flag

# Create a list of all the available functions for LLM to use
available_functions = types.Tool(
function_declarations=[
    schema_get_files_info,
    schema_get_file_content,
    schema_run_python_file,
    schema_write_file,
    ]
)   

# Content generation function to be called by main() iteratively
def generate_content(client, messages, verbose):

     # Send the request to the model with the conversation contents
    resp = client.models.generate_content(
        model=model_name,
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions], system_instruction=system_prompt
            ),
    )

    if verbose: # Checks if 'verbose' flag passed as a command-line argument
        print('Verbose mode on')  

        # getattr() function tries to find attribute and if not found return default value instead of crashing program
        meta = getattr(resp, "usage_metadata", None) 
        prompt_tokens = getattr(meta, "prompt_token_count", "unknown") if meta else "unknown"
        resp_tokens = getattr(meta, "candidates_token_count", "unknown") if meta else "unknown"
        
        print(f"Prompt tokens: {prompt_tokens}")
        print(f"Response tokens: {resp_tokens}")

    # Append candidates (response variation) to messages so included in conversation
    if resp.candidates:
        for candidate in resp.candidates:
            messages.append(candidate.content)

    # Confirm whether finished and return text so main() can decide to stop
    if not resp.function_calls and resp.text:
        return resp.text 
    
    if resp.function_calls:
       
        # Append candidates (response variation) to messages so included in conversation
        function_responses = []
        for function_call_part in resp.function_calls:
            function_call_result = call_function(function_call_part, verbose=verbose)
            function_responses.append(function_call_result.parts[0])
        
        if len(function_responses) != 0:
            messages.append(types.Content(role='user',parts=function_responses))

        return None

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

    # Limit loop to 20 iterations as specificied in config.py
    iters = 0
    while True:
        iters += 1
        if iters > MAX_ITERS:
            print(f"Maximum iterations ({MAX_ITERS}) reached.")
            sys.exit(1)

        try:
            final_response = generate_content(client, messages, args.verbose)
            if final_response:
                print("Final response:")
                print(final_response)
                break
        except Exception as e:
            print(f"Error in generate_content: {e}")

if __name__ == "__main__":             # Only run main when executed as a script
    main()