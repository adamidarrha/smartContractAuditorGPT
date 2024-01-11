def count_characters(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            contents = file.read()
            return len(contents)
    except FileNotFoundError:
        print("File not found.")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

# Replace 'your_file.txt' with the path to your file
file_path = 'prompt.md'
char_count = count_characters(file_path)

if char_count is not None:
    print(f"The file has {char_count} characters.")
