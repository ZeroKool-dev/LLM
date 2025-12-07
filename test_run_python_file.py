from functions.run_python_file import run_python_file


def print_result(label, working_directory, file_path, args=None):
    result = run_python_file(working_directory, file_path, args=args)
    print(f"{label}:\n{result}\n")


if __name__ == "__main__":
    print_result("Usage output", "calculator", "main.py")
    print_result("Simple calculation", "calculator", "main.py", ["3 + 5"])
    print_result("Calculator tests", "calculator", "tests.py")
    print_result("Outside working dir", "calculator", "../main.py")
    print_result("Missing file", "calculator", "nonexistent.py")
    print_result("Not a Python file", "calculator", "lorem.txt")
