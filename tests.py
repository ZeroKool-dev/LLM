from functions.get_file_content import get_file_content


def print_result(label, working_directory, file_path):
    print(f'get_file_content("{working_directory}", "{file_path}"):\nResult for {label}:')
    result = get_file_content(working_directory, file_path)
    print(result)
    print()


if __name__ == "__main__":
    print_result('"main.py"', "calculator", "main.py")
    print_result('"pkg/calculator.py"', "calculator", "pkg/calculator.py")
    print_result('"/bin/cat"', "calculator", "/bin/cat")
    print_result('"pkg/does_not_exist.py"', "calculator", "pkg/does_not_exist.py")
