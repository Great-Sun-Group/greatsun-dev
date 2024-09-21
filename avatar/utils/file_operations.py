import os
import json
import time
import subprocess
import sys
from collections import deque


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

    def process_queue(self):
        while self.queue:
            op = self.queue.popleft()
            if all(dep in self.results for dep in op.dependencies):
                result = perform_file_operation(op.operation, *op.args)
                self.results[op] = result
                time.sleep(0.1)  # Small delay to allow file system to update
            else:
                self.queue.append(op)
        return self.results


def load_initial_context():
    initial_context = [
        read_file("avatar/context/avatar_orientation.md"),
        read_file("avatar/context/response_instructions.txt"),
        "*** README.md ***",
        read_file("README.md"),
        "*** credex-core/README.md ***",
        read_file("credex-ecosystem/credex-core/README.md"),
        "*** credex-ecosystem/vimbiso-pay/README.md ***",
        read_file("credex-ecosystem/vimbiso-pay/README.md"),
        "*** FULL DIRECTORY TREE ***",
        json.dumps(get_directory_tree('/workspaces/greatsun-dev'), indent=2),
        "*** avatar/context/current_project.md ***",
        read_file("avatar/context/current_project.md"),
        f"*** MESSAGE FROM DEVELOPER @{os.environ.get('GH_USERNAME')} ***",
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
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'w') as file:
            file.write(file_content)
        return True
    except Exception as e:
        print(f"Error writing to file {file_path}: {str(e)}")
        return False


def get_directory_tree(path):
    """
    Recursively get the directory structure as a dictionary, excluding only specific system and hidden files.

    Args:
    path (str): Path to the directory

    Returns:
    dict: Directory structure
    """
    tree = {}
    excluded_files = {'.DS_Store', 'Thumbs.db', '.gitignore', '.gitattributes'}

    try:
        for entry in os.scandir(path):
            if entry.is_dir():
                # Exclude .git directory
                if entry.name == '.git':
                    continue
                subtree = get_directory_tree(entry.path)
                tree[entry.name] = subtree
            elif entry.is_file():
                # Exclude specific files
                if entry.name not in excluded_files:
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
    Various: Depends on the operation performed
    """
    max_attempts = 3
    delay = 0.1

    for attempt in range(max_attempts):
        try:
            if operation == 'read':
                return read_file(args[0])
            elif operation == 'write':
                return write_file(args[0], args[1])
            elif operation == 'append':
                with open(args[0], 'a') as f:
                    f.write(args[1])
                return True
            elif operation == 'delete':
                os.remove(args[0])
                return True
            elif operation in ['rename', 'move']:
                os.rename(args[0], args[1])
                return True
            elif operation == 'list_directory':
                return os.listdir(args[0])
            elif operation == 'create_directory':
                os.makedirs(args[0], exist_ok=True)
                return True
            else:
                raise ValueError(f"Unknown operation: {operation}")
        except Exception as e:
            if attempt < max_attempts - 1:
                time.sleep(delay)
                delay *= 2  # Exponential backoff
            else:
                print(f"Error performing {operation}: {str(e)}")
                return False

    return False  # This line should never be reached, but it's here for completeness


def install_package(package_name: str) -> bool:
    try:
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", package_name])
        print(f"Successfully installed {package_name}")
        print("Exiting to reset. Run `avatar up` again to launch.")
        sys.exit(1)
    except subprocess.CalledProcessError as e:
        print(f"Failed to install {package_name}: {e}")
        return False
