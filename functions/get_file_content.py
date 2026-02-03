import os
from google.genai import types
from config import MAX_CHARACTERS

def get_file_content(working_directory, file_path):
    wkdpath = os.path.abspath(working_directory)
    final_path = os.path.normpath(os.path.abspath(os.path.join(wkdpath, file_path)))
    valid_final_path = os.path.commonpath([wkdpath, final_path]) == wkdpath
    if not valid_final_path:
        raise ValueError(f'Error: Cannot read "{file_path}" as it is outside the permitted working directory')
    if not os.path.isfile(final_path):
        raise TypeError(f' Error: File not found or is not a regular file: "{file_path}"')
    with open(final_path, "r") as f:
        file_contents = f.read(MAX_CHARACTERS)
        extra_characters = f.read(1)
        if extra_characters:
            file_contents += f'\n\n[...File "{file_path}" truncated at {MAX_CHARACTERS} characters]'
    return file_contents

    
schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="read and print up to 10000 characters from a file",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="a specific file to look for, open, and read within the 'working directory'. (Default is the working directory)"
            ),
        },
        required=["file_path"]
    ),
)
