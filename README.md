# Repository Code Splitter

This Python script processes a repository to extract source code files with specific extensions and saves them into multiple JSON files. Each JSON file is limited to a specified maximum size, and large files can be excluded from processing based on their size.

## Features
- Extracts files with specified extensions from a repository.
- Splits content into multiple JSON files, each under a specified size limit.
- Excludes files larger than a specified size.
- Handles nested directories recursively.
- Logs errors for unreadable files.

## Requirements
- Python 3.x
- No external libraries required (uses standard Python modules like `os` and `json`).

## Usage

### 1. Clone the Repository
```bash
git clone https://github.com/takurot/repository-code-splitter.git
cd repository-code-splitter
```

### 2. Update Parameters
Modify the script's `main` section to fit your needs:

- **`repository_path`**: Path to the repository to process.
- **`output_directory`**: Directory where the JSON files will be saved.
- **`max_file_size_mb`**: Maximum size for each JSON file (in MB).
- **`exclude_file_size_mb`**: Exclude files larger than this size (in MB).
- **`target_file_extensions`**: List of file extensions to include.

### 3. Run the Script
```bash
python repository_code_splitter.py
```

### Example
```python
repository_path = "./my-repo"            # Directory to process
output_directory = "./json_output"      # Output directory for JSON files
max_file_size_mb = 5                    # Maximum JSON file size in MB
exclude_file_size_mb = 0.5              # Exclude files larger than 0.5MB
target_file_extensions = [".py", ".ts", ".json", ".cpp"]  # File extensions to include
```

### 4. Output
The output JSON files will be saved in the specified output directory, with filenames like:
```
1_repository_code.json
2_repository_code.json
...
```

Each JSON file contains the following structure:
```json
{
  "files": [
    {
      "path": "relative/path/to/file",
      "content": "file content as a string"
    },
    {
      "path": "relative/path/to/another/file",
      "error": "Error message if the file could not be read"
    }
  ]
}
```

## Parameters
| Parameter                | Description                                     | Default                |
|--------------------------|-------------------------------------------------|------------------------|
| `repository_path`        | Path to the repository to process               | `./extensions`         |
| `output_directory`       | Directory where JSON files are saved            | `./json_output`        |
| `max_file_size_mb`       | Maximum size for each JSON file (in MB)         | `5`                    |
| `exclude_file_size_mb`   | Exclude files larger than this size (in MB)     | `0.5`                  |
| `target_file_extensions` | List of file extensions to include              | `[".py", ".ts", ".tsx", ".json"]` |

## Handling Large Files
Files larger than `exclude_file_size_mb` are automatically skipped. A message will be logged for each skipped file.

Example:
```
Skipping large file: relative/path/to/large_file.py (>0.5 MB)
```

## License
This project is licensed under the MIT License. See the `LICENSE` file for details.

## Contribution
Contributions are welcome! Please submit a pull request or create an issue to report bugs or suggest enhancements.
