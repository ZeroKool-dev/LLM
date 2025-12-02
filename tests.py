from functions.get_files_info import get_files_info


def print_result(label, working_directory, directory):
    print(f'get_files_info("{working_directory}", "{directory}"):\nResult for {label} directory:')
    result = get_files_info(working_directory, directory)
    if result.startswith("Error:"):
        print(f"    {result}\n")
        return

    for line in result.splitlines():
        print(f" {line}")
    print()


if __name__ == "__main__":
    print_result("current", "calculator", ".")
    print_result("'pkg'", "calculator", "pkg")
    print_result("'/bin'", "calculator", "/bin")
    print_result("'../'", "calculator", "../")
