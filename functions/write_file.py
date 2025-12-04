import os


def write_file(working_directory, file_path, content):
    abs_working_dir = os.path.abspath(working_directory)
    abs_file_path = os.path.abspath(os.path.join(working_directory, file_path))
    if not abs_file_path.startswith(abs_working_dir):
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    if os.path.isdir(abs_file_path):
        return f'Error: "{file_path}" is a directory, not a file'
    try:
        dirpath = os.path.dirname(abs_file_path)
        if dirpath:
            os.makedirs(dirpath, exist_ok=True)
        with open(abs_file_path, "w") as f:
            f.write(content)
        return (
            f'Successfully wrote to "{file_path}" '
            f"({len(content)} characters written)"
        )
    except Exception as e:
        return f'Error: writing file "{file_path}": {e}'
