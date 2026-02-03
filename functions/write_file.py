import os
from google.genai import types

def write_file(working_directory, file_path, content):
    wkdpath = os.path.abspath(working_directory)
    final_path = os.path.normpath(os.path.abspath(os.path.join(wkdpath, file_path)))
    valid_final_path = os.path.commonpath([wkdpath, final_path]) == wkdpath
    if not valid_final_path:
        raise ValueError(f'Error: Cannot read "{file_path}" as it is outside the permitted working directory')
    if os.path.isdir(final_path):
        raise ValueError(f'Error: "{final_path}" as it is a directory')
    parent_dir = os.path.dirname(final_path)
    os.makedirs(parent_dir, exist_ok=True)
    with open(final_path, "w") as f:
        owdoc = f.write(content)
        if owdoc > 0:
            return(f'Successfully wrote to "{final_path}" ({len(content)} characters written)')
        else:
            return(f'{final_path} was succesfully created, but nothing was written to it')


schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="open a current file or create a new file at working directory/file_path name and write the content to that file.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="the file name withing the working directory. working directory is relative to the default working directory.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="the exact string that will be written to the file at working directory/file_path. if a file exists and has information already inside. overwrite the file with the content",
            ),
        },
    required=["file_path", "content"]
    ),
)

