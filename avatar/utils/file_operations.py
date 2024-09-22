import os
import json
import time
from collections import deque
from pathlib import Path
from constants import BASE_DIR


class FileOperation:
    def __init__(self, operation, *args):
        self.operation = operation
        self.args = args
        self.dependencies = set()


class FileOperationQueue:
    def __init__(self):
        self.queue = deque()
        self.results = {}

    def add_operation(self, operation, *args):
        op = FileOperation(operation, *args)
        self.queue.append(op)
        return op

    def add_dependency(self, operation, dependency):
        operation.dependencies.add(dependency)

    def process_queue(self, conversation_thread):
        while self.queue:
            op = self.queue.popleft()
            if all(dep in self.results for dep in op.dependencies):
                result = perform_file_operation(op.operation, *op.args)
                self.results[op] = result
                conversation_thread += f"Operation: {op.operation}\n"
                conversation_thread += f"Arguments: {op.args}\n"
                conversation_thread += f"Result: {result}\n\n"
                time.sleep(0.1)  # Small delay to allow file system to update
            else:
                self.queue.append(op)
        return self.results, conversation_thread


def load_initial_context():
    initial_context = [
        read_file(BASE_DIR / "avatar/context/avatar_orientation.md"),
        read_file(BASE_DIR / "avatar/utils/response_instructions.txt"),
        f"\n\n*** README.md ***\n\n",
        read_file(BASE_DIR / "README.md"),
        f"\n\n*** credex-core/README.md ***\n\n",
        read_file(BASE_DIR / "credex-ecosystem/credex-core/README.md"),
        f"\n\n*** credex-ecosystem/vimbiso-pay/README.md ***\n\n",
        read_file(BASE_DIR / "credex-ecosystem/vimbiso-pay/README.md"),
        f"*** FULL DIRECTORY TREE ***\n\n",
        json.dumps(get_directory_tree(BASE_DIR), indent=2),
        f"\n\n*** avatar/context/current_project.md ***\n\n",
        read_file(BASE_DIR / "avatar/context/current_project.md"),
        f"\n\n*** MESSAGE FROM DEVELOPER @{
            os.environ.get('GH_USERNAME')} ***\n\n",
    ]
    return ''.join(initial_context)


def read_file(file_path):
    """
    Function to read and return contents of a file, with solid error handling.
    """
    try:
        with open(file_path, 'r') as file:
            content = file.read()
        return content
    except FileNotFoundError:
        return f"File not found: {file_path}"
    except Exception as e:
        return f"Error reading file: {str(e)}"


def write_file(file_path, file_content):
    """
    Function that will create the file if it doesn't exist and write over what is there if it does exist,
    with solid error handling.
    """
    try:
        file_path = Path(file_path)
        file_path.parent.mkdir(parents=True, exist_ok=True)
        with file_path.open('w') as file:
            file.write(file_content)
        return True
    except Exception as e:
        print(f"Error writing to file {file_path}: {str(e)}")
        return False


def get_directory_tree(path):
    """
    Recursively get the directory structure as a dictionary, excluding unnecessary files and directories.

    Args:
    path (Path): Path to the directory

    Returns:
    dict: Directory structure
    """
    tree = {}
    excluded_files = {
        '.DS_Store', 'Thumbs.db', '.gitignore', '.gitattributes',
        '.env', '.coverage', '*.pyc', '*.pyo', '*.whl', '*.egg',
        '*.log', '*.zip', '*.tar.gz', '*.rar', '*.db', '*.sqlite'
    }
    excluded_dirs = {
        '__pycache__', '.git', '.svn', '.hg', 'node_modules',
        'venv', 'env', 'build', 'dist', '.vscode', '.idea',
        'tmp', 'temp', 'htmlcov'
    }

    try:
        for entry in path.iterdir():
            if entry.is_dir():
                if entry.name in excluded_dirs or entry.name.endswith('.egg-info'):
                    continue
                subtree = get_directory_tree(entry)
                if subtree:  # Only add non-empty directories
                    tree[entry.name] = subtree
            elif entry.is_file():
                if any(entry.name.endswith(ext) for ext in excluded_files):
                    continue
                tree[entry.name] = None
    except Exception as e:
        print(f"Error getting directory tree for {path}: {str(e)}")

    return tree


def perform_file_operation(operation, *args):
    """
    Function to perform various file operations with error handling and retries.

    Args:
    operation (str): The type of operation to perform ('read', 'write', 'append', 'delete', 'rename', 'move', 'list_directory', 'create_directory')
    *args: Arguments specific to each operation

    Returns:
    list: conversation_thread containing the results of the operation
    """
    max_attempts = 3
    delay = 0.1
    conversation_thread = []

    for attempt in range(max_attempts):
        try:
            if operation == 'read':
                read_file_contents = read_file(args[0])
                conversation_thread.append(
                    f"Read file: {args[0]}\nContents: {read_file_contents}")
            elif operation == 'write':
                write_response = write_file(args[0], args[1])
                conversation_thread.append(
                    f"Write to file: {args[0]}\nSuccess: {write_response}")
            elif operation == 'append':
                with open(args[0], 'a') as f:
                    f.write(args[1])
                conversation_thread.append(
                    f"Append to file: {args[0]}\nAppended content: {args[1]}")
            elif operation == 'delete':
                Path(args[0]).unlink()
                conversation_thread.append(
                    f"Delete file: {args[0]}\nSuccess: True")


            elif operation in ['rename', 'move']:
                Path(args[0]).rename(args[1])
                conversation_thread.append(f"{operation.capitalize()} file from {
                                           args[0]} to {args[1]}\nSuccess: True")
            elif operation == 'list_directory':
                directory_contents = list(Path(args[0]).iterdir())
                conversation_thread.append(
                    f"List directory: {args[0]}\nContents: {directory_contents}")
            elif operation == 'create_directory':
                Path(args[0]).mkdir(parents=True, exist_ok=True)
                conversation_thread.append(
                    f"Create directory: {args[0]}\nSuccess: True")
            else:
                raise ValueError(f"Unknown operation: {operation}")

            return conversation_thread  # Return after successful operation
        except Exception as e:
            if attempt < max_attempts - 1:
                time.sleep(delay)
                delay *= 2  # Exponential backoff
            else:
                error_message = f"Error performing {operation} on {args}: {str(e)}"
                print(error_message)
                conversation_thread.append(error_message)
                return conversation_thread  # Return after all attempts failed

    # This line should never be reached, but it's here for completeness
    return conversation_thread

def is_path_allowed(path: str) -> bool:
    """Check if the given path is within the allowed directory."""
    try:
        path = Path(path).resolve()
        return BASE_DIR in path.parents or path == BASE_DIR
    except Exception as e:
        print(f"Error validating path: {e}")
        return False

def validate_file_operation(operation: str, path: str, new_path: str = None) -> bool:
    """Validate file operations to ensure they're within allowed directories."""
    if not is_path_allowed(path):
        print(f"Attempted operation outside allowed directory: {path}")
        return False

    if new_path and not is_path_allowed(new_path):
        print(f"Attempted operation outside allowed directory: {new_path}")
        return False

    return True
