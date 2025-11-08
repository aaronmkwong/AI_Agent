# build a “tool-call” function an LLM can use to list a directory’s contents as plain text
# LLMs operate on strings, so everything—including errors—must be returned as strings

import os 

def get_files_info(working_directory, directory="."):
    
    # resolve absolute paths for the working dir and the target (joined) path
    abs_working = os.path.abspath(working_directory)  
    abs_target = os.path.abspath(os.path.join(working_directory, directory))
    dir_info = []
    
    # guardrail: block access outside the working directory boundary
    if not abs_target.startswith(abs_working):
          return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    
    # validate the target is a directory
    if not os.path.isdir(abs_target):
          return f'Error: "{directory}" is not a directory'
           
    try:
        
        # build one line per entry with size and directory flag
        for item in os.listdir(abs_target):
          item_path = os.path.join(abs_target, item)
          dir_info.append(f'- {item}: file_size={os.path.getsize(item_path)} bytes, is_dir={os.path.isdir(item_path)}')
         
         # return a single string (LLM-friendly)
        return '\n'.join(dir_info)
    
    except Exception as e:
        # always return errors as strings
        return f'Error: {e}'  
    
    
     
    
