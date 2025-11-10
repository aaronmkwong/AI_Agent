import os
import subprocess
import sys

def run_python_file(working_directory, file_path, args=[]):

    # compute absolute paths to prevent path traversal issues
    abs_working = os.path.abspath(working_directory)  
    abs_target = os.path.abspath(os.path.join(working_directory, file_path))
    
    # ensure target stays within the allowed working directory
    if not abs_target.startswith(abs_working):
          return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    
    # ensure the file exists (after resolving to absolute path)
    if not os.path.isfile(abs_target):
          return f'Error: File "{file_path}" not found.'
    
    # ensure it's a Python file by extension
    if not abs_target.endswith('.py'):
          return f'Error: "{file_path}" is not a Python file.'
           
    try:

        # build the command:
        # - sys.executable guarantees we use the current Python interpreter
        # - file_path can be relative because cwd is set to working_directory
        # - append any extra args passed to the script
        cmd = [sys.executable,file_path] + list(args)

        # run the process:
        # - timeout caps long-running scripts
        # - capture_output grabs both stdout and stderr
        # - text=True decodes bytes to str using system default encoding
        # - cwd confines execution to the working directory
        completed_process = subprocess.run(cmd, timeout=30, capture_output=True, cwd=working_directory, text=True)
        
        # normalize None to empty strings for safe checks/concatenation
        out = completed_process.stdout or ""
        err = completed_process.stderr or ""

        # if nothing was produced on either stream
        if out == "" and err == "":
            return "No output produced."

        # format output consistently with required prefixes
        lines = [f"STDOUT: {out}", f"STDERR: {err}"]
      
        # include exit code info on failure (non-zero return code)
        if completed_process.returncode != 0:
            lines.append(f"Process exited with code {completed_process.returncode}")

        # join with newlines so each section is readable    
        return "\n".join(lines)
        
    except Exception as e:
        # convert any unexpected issues into a user-facing error string
        return f'Error: executing Python file: {e}'  