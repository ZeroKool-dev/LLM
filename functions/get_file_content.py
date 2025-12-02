import os

from config import MAX_CHARS


def get_file_content(working_directory, file_path):
    """
    Return the contents of a file located within working_directory.
    Enforces that the target path stays inside working_directory boundaries and truncates long files.
    """
    try:
        base_dir = os.path.abspath(working_directory)
        target_path = os.path.abspath(os.path.join(working_directory, file_path))

        if os.path.commonpath([base_dir, target_path]) != base_dir:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

        if not os.path.isfile(target_path):
            return f'Error: File not found or is not a regular file: "{file_path}"'

        with open(target_path, "r") as file:
            content = file.read(MAX_CHARS + 1)

        if len(content) > MAX_CHARS:
            truncated = content[:MAX_CHARS]
            return f'{truncated}[...File "{file_path}" truncated at {MAX_CHARS} characters]'

        return content
    except Exception as exc:
        return f"Error: {exc}"
