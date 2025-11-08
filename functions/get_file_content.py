# ...

from functions.config import MAX_CHARS
import os 

def get_file_content(working_directory, file_path):
    
    # resolve absolute paths for the working dir and the target (joined) path
    abs_working = os.path.abspath(working_directory)  
    abs_target = os.path.abspath(os.path.join(working_directory, file_path))
    
    # guardrail: block access outside the working directory boundary
    if not abs_target.startswith(abs_working):
          return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    
    # validate the target is a file
    if not os.path.isfile(abs_target):
          return f'Error: File not found or is not a regular file: "{file_path}"'
           
    try:
        
        with open(abs_target, "r") as f:
             file_content_string = f.read(MAX_CHARS)
        
        if len(file_content_string) == MAX_CHARS:
            return file_content_string + f'...File "{file_path}" truncated at 10000 characters'
        
        else:
             return file_content_string
    
    except Exception as e:
        # always return errors as strings
        return f'Error: {e}'  
    
    
     
    
