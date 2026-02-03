from functions.get_file_content import get_file_content

tests = [
    ("calculator", "main.py"),
    ("calculator", "pkg/calculator.py"),
    ("calculator", "/bin/cat"),
    ("calculator", "pkg/does_not_exist.py"),
]

for test in tests:
    try:
        working_directory, file_name = test
        print(get_file_content(working_directory, file_name))
    except Exception as e:
        print(f"Error: {e}")
