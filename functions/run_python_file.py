import os
import shutil
import subprocess
import sys

from google.genai import types


def run_python_file(working_directory, file_path, args=None):
    abs_working_dir = os.path.abspath(working_directory)
    abs_file_path = os.path.abspath(os.path.join(working_directory, file_path))

    if not abs_file_path.startswith(abs_working_dir):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

    if not file_path.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file.'

    if not os.path.exists(abs_file_path):
        return f'File "{file_path}" not found'

    if os.path.isdir(abs_file_path):
        return f'Error: "{file_path}" is a directory, not a file'

    extra_args = []
    if args is not None:
        if isinstance(args, (list, tuple)):
            extra_args = list(args)
        else:
            extra_args = [str(args)]

    python_cmd = shutil.which("python") or sys.executable

    try:
        result = subprocess.run(
            [python_cmd, abs_file_path, *extra_args],
            capture_output=True,
            text=True,
            cwd=abs_working_dir,
            timeout=30,
        )
    except Exception as e:
        return f"Error: executing Python file: {e}"

    stdout = result.stdout or ""
    stderr = result.stderr or ""
    output_lines = []

    if result.returncode != 0:
        output_lines.append(f"Process exited with code {result.returncode}")

    if not stdout and not stderr:
        output_lines.append("No output produced")
        return "\n".join(output_lines)

    output_lines.append(f"STDOUT:\n{stdout}".rstrip())
    output_lines.append(f"STDERR:\n{stderr}".rstrip())
    return "\n".join(output_lines).rstrip()


schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Executes a Python file with optional arguments, constrained to the working directory and with a timeout.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the Python file to execute, relative to the working directory.",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                description="Optional list of arguments to pass to the Python file.",
                items=types.Schema(type=types.Type.STRING),
            ),
        },
    ),
)
