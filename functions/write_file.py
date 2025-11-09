import os

def write_file(working_directory, file_path, content):

    # resolve absolute paths for the working dir and the target (joined) path
    abs_working = os.path.abspath(working_directory)  
    abs_target = os.path.abspath(os.path.join(working_directory, file_path))
    
    # guardrail: block access outside the working directory boundary
    if os.path.commonpath([abs_working, abs_target]) != abs_working:
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

    try:
    
        # create parent directory input is not null and not exist in os
        parent_dir = os.path.dirname(abs_target)
        if parent_dir and not os.path.isdir(parent_dir):
            os.makedirs(parent_dir, exist_ok=True)

        # create and/or over write file
        with open(abs_target, "w") as f:
            f.write(content)

        # success notificaiton for LLM
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'

    except Exception as e:
        # always return errors as strings
        return f'Error: {e}'
     