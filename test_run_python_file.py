from functions.run_python_file import run_python_file

tests = [
    ("calculator", "main.py"),
    ("calculator", "main.py", ["3 + 5"]),
    ("calculator", "tests.py"),
    ("calculator", "../main.py"),
    ("calculator", "nonexistent.py"),
    ("calculator", "lorem.txt"),
]

for test in tests:
    try:
        working_directory, file_name = test[:2]
        arg = test[2] if len(test) > 2 else None
        print(run_python_file(working_directory, file_name, args=arg))
    except Exception as e:
        print(f"Error: {e}")