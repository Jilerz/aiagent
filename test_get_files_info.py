from functions.get_files_info import get_files_info

tests = [
    ("calculator", "."),
    ("calculator", "pkg"),
    ("calculator", "/bin"),
    ("calculator", "../"),
]

for test in tests:
    try:
        working_dir, directory = test
        get_files_info(working_dir, directory)
    except Exception as e:
        print(f"Error: {e}")



