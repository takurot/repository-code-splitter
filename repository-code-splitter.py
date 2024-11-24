import os
import json

def write_code_to_json_split(repo_path, output_dir, max_size_mb=10, target_extensions=None, exclude_file_size_mb=5):
    """
    Reads all files in a repository with specific extensions and writes their contents
    to multiple JSON files, each under the specified maximum size (in MB).
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    current_file_size = 0
    file_counter = 1
    current_json = {"files": []}

    def save_current_json():
        """
        Saves the current JSON data to a file.
        """
        nonlocal file_counter, current_file_size, current_json
        file_path = os.path.join(output_dir, f"{file_counter}_repository_code.json")
        with open(file_path, "w", encoding="utf-8") as json_file:
            json.dump(current_json, json_file, ensure_ascii=False, indent=4)
        current_file_size = 0
        file_counter += 1
        current_json = {"files": []}

    def add_file_to_json(file_path, relative_path):
        """
        Adds the content of a file to the current JSON data.
        """
        nonlocal current_file_size, current_json

        try:
            # Check the file size in MB
            if os.path.getsize(file_path) > exclude_file_size_mb * 1024 * 1024:
                print(f"Skipping large file: {relative_path} (>{exclude_file_size_mb} MB)")
                return

            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
                file_data = {
                    "path": relative_path,
                    "content": content
                }

                file_size = len(json.dumps(file_data).encode("utf-8"))

                # Check if adding this file exceeds the maximum JSON size
                if current_file_size + file_size > max_size_mb * 1024 * 1024:
                    save_current_json()

                current_json["files"].append(file_data)
                current_file_size += file_size
        except Exception as e:
            file_data = {
                "path": relative_path,
                "error": f"Unable to read file: {e}"
            }
            current_json["files"].append(file_data)
            current_file_size += len(json.dumps(file_data).encode("utf-8"))

    def process_directory(dir_path, relative_path):
        """
        Recursively processes a directory.
        """
        for item in sorted(os.listdir(dir_path)):
            item_path = os.path.join(dir_path, item)
            item_relative_path = os.path.join(relative_path, item)
            if os.path.isfile(item_path):
                if target_extensions is None or any(item_path.endswith(ext) for ext in target_extensions):
                    add_file_to_json(item_path, item_relative_path)
            elif os.path.isdir(item_path):
                process_directory(item_path, item_relative_path)

    # Start processing the repository
    process_directory(repo_path, "")

    # Save the last JSON file
    if current_json["files"]:
        save_current_json()

# Usage example
if __name__ == "__main__":
    repository_path = "./extensions"  # Replace with your repository path
    output_directory = "./json_output"  # Directory where JSON files will be saved
    max_file_size_mb = 5  # Maximum size per JSON file in MB
    exclude_file_size_mb = 0.3  # Exclude files larger than this size in MB
    target_file_extensions = [".py", ".ts", ".tsx", ".yaml", ".yml", ".c", ".cpp", ".h", ".hpp", ".json"]  # Specify target extensions
    write_code_to_json_split(repository_path, output_directory, max_file_size_mb, target_file_extensions, exclude_file_size_mb)
    print(f"JSON files created in: {output_directory}")
