from functions.write_file import write_file

tests = [
    ("calculator", "lorem.txt", "wait, this isn't lorem ipsum"),
    ("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet"),
    ("calculator", "/tmp/temp.txt", "this should not be allowed"),
]

for test in tests:
    try:
        working_directory, file_path, content = test
        write_file(working_directory, file_path, content)
    except Exception as e:
        print(f"Error: {e}")