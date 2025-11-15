from google.genai import types 
from functions.get_file_content import get_file_content
from functions.get_files_info import get_files_info
from functions.write_file import write_file
from functions.run_python_file import run_python_file

# handles the abstract task of calling one of our four functions
def call_function(function_call_part, verbose=False):

    # to resolve the function name string to the actual callable object
    # a dictionary is a lookup table: #map "name string" → real function.
    # then func = FUNCTIONS[function_call_part.name] and call func(**kwargs).
    # without map Python has no idea which callable the string refers to

    FUNCTIONS = {
        "get_file_content": get_file_content,
        "get_files_info": get_files_info,
        "write_file": write_file,
        "run_python_file": run_python_file,
    }

    # get string name of function and dictionary of named arguments to the function
    function_name = function_call_part.name # string

    if function_name not in FUNCTIONS:
        return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_name,
                response={"error": f"Unknown function: {function_name}"},
            )
        ],
        )
    
    function = FUNCTIONS[function_name] # call function (not as string)
    func_kwargs = dict(function_call_part.args)

    # Normalize model-provided args to the exact parameter names our tools expect
    # LLMs can vary wording ("directory", "path") even if we intend "file_path" 
    # This is an interface boundary: upstream is probabilistic (LLM), downstream is strict (Python call), so normalization is the adapter

    # Ensure the callable receives 'file_path' regardless of how the model named it
    if function_name == "run_python_file":
        if "file_path" not in func_kwargs:
            if "directory" in func_kwargs:
                func_kwargs["file_path"] = func_kwargs.pop("directory")
            elif "path" in func_kwargs:
                func_kwargs["file_path"] = func_kwargs.pop("path")

    # Same normalization for this tool: it also expects 'file_path'
    elif function_name == "get_file_content":
        if "file_path" not in func_kwargs:
            if "directory" in func_kwargs:
                func_kwargs["file_path"] = func_kwargs.pop("directory")
            elif "path" in func_kwargs:
                func_kwargs["file_path"] = func_kwargs.pop("path")

    # Map alternative names to 'file_path' so signature matches exactly
    elif function_name == "write_file_content":
        # ensure keys match your function’s signature, e.g. file_path and content
        if "file_path" not in func_kwargs and "directory" in func_kwargs:
            func_kwargs["file_path"] = func_kwargs.pop("directory")

    # always enforce the working directory for our tools
    # add "working_directory" argument to dictionary as  LLM doesn't control it
    func_kwargs["working_directory"] = "./calculator"

    if verbose:
        print(f"Calling function: {function_name}({func_kwargs})")

    else:
        print(f" - Calling function: {function_name}")

    
    function_result = function(**func_kwargs)

    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_name,
                # from_function_response requires the response to be a dictionary, so  shove the string result into a "result" field
                response={"result": function_result},
            )
        ],
    )


    




         

