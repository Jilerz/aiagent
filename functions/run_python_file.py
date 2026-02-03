import os
import subprocess
from google.genai import types

def run_python_file(working_directory, file_path, args=None):
    try:
        wkpath = os.path.abspath((working_directory))
        final_path = os.path.normpath(os.path.abspath(os.path.join(wkpath, file_path)))
        valid_final_path = os.path.commonpath([wkpath, final_path]) == wkpath
        if not valid_final_path:
            raise ValueError(f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory')
        if not os.path.isfile(final_path):
            raise TypeError(f'Error: "{file_path}" does not exist or is not a regular file')
        if not final_path.endswith(".py"):
            raise TypeError(f'Error: "{file_path}" is not a Python file')
        command = ["python", final_path]
        if args != None:
            command.extend(args)
        subcommand = subprocess.run(command,cwd=wkpath, text=True, timeout=30, capture_output=True)
        output_string = ""
        if subcommand.returncode != 0:
            output_string += (f'Process exited with code {subcommand.returncode}\n')
        if not subcommand.stdout and not subcommand.stderr:
            output_string += "No output produced\n"
        else:
            if subcommand.stdout:
                output_string += f"STDOUT: {subcommand.stdout.strip()}\n"
            if subcommand.stderr:
                output_string += f"STDERR: {subcommand.stderr.strip()}\n"
        return output_string
    except Exception as e:
        return(f"Error: {e}")
    


schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="call the function and paste results of the run_python_file function",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="the file to run in the working directory. the working directory is relative to the default working directory.",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(
                    type=types.Type.STRING,
                ),
                description="an optional argument sometimes provided for specific python files required input."
            ),
        },
        required=["file_path"]     
    ),
)
