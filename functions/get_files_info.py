import os


def get_files_info(working_directory, directory="."):
    """
    Return a string describing the contents of a directory relative to working_directory.
    The result lists one entry per line in the format:
    - filename: file_size=123 bytes, is_dir=False
    """
    try:
        base_dir = os.path.abspath(working_directory)
        target_path = os.path.abspath(os.path.join(working_directory, directory))

        # Ensure the target path stays within the permitted working directory.
        common_path = os.path.commonpath([base_dir, target_path])
        if common_path != base_dir:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

        if not os.path.isdir(target_path):
            return f'Error: "{directory}" is not a directory'

        entries = []
        for entry in sorted(os.listdir(target_path)):
            entry_path = os.path.join(target_path, entry)
            size = os.path.getsize(entry_path)
            is_dir = os.path.isdir(entry_path)
            entries.append(f"- {entry}: file_size={size} bytes, is_dir={is_dir}")

        return "\n".join(entries)
    except Exception as exc:  # Catch all errors and return as strings for the LLM to handle.
        return f"Error: {exc}"
