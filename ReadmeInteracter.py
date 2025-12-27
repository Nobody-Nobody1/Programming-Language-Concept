import os

def display_readme(file_path="README.md"):
    if not os.path.exists(file_path):
        print(f"Error: {file_path} not found.")
        return
    
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
        print(content)
    except Exception as e:
        print(f"Error reading {file_path}: {e}")