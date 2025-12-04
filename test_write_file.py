from functions.write_file import write_file


def print_result(working_directory, file_path, content):
    result = write_file(working_directory, file_path, content)
    print(f'write_file("{working_directory}", "{file_path}", "{content}"):\n{result}\n')


if __name__ == "__main__":
    print_result("calculator", "lorem.txt", "wait, this isn't lorem ipsum")
    print_result("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet")
    print_result("calculator", "/tmp/temp.txt", "this should not be allowed")
