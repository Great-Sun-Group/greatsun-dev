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
        read_file("avatar/context/avatar_orientation.md"),
        read_file("avatar/utils/response_instructions.txt"),
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
        f"\n\n*** MESSAGE FROM DEVELOPER @{os.environ.get('GH_USERNAME')} ***",
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
    Recursively get the directory structure as a dictionary, excluding unnecessary files and directories.

    Args:
    path (str): Path to the directory

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
        for entry in os.scandir(path):
            if entry.is_dir():
                if entry.name in excluded_dirs:
                    continue
                if entry.name.endswith('.egg-info'):
                    continue
                subtree = get_directory_tree(entry.path)
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
                os.remove(args[0])
                conversation_thread.append(
                    f"Delete file: {args[0]}\nSuccess: True")
            elif operation in ['rename', 'move']:
                os.rename(args[0], args[1])
                conversation_thread.append(f"{operation.capitalize()} file from {
                                           args[0]} to {args[1]}\nSuccess: True")
            elif operation == 'list_directory':
                directory_contents = os.listdir(args[0])
                conversation_thread.append(
                    f"List directory: {args[0]}\nContents: {directory_contents}")
            elif operation == 'create_directory':
                os.makedirs(args[0], exist_ok=True)
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
                error_message = f"Error performing {operation}: {str(e)}"
                print(error_message)
                conversation_thread.append(error_message)
                return conversation_thread  # Return after all attempts failed

    # This line should never be reached, but it's here for completeness
    return conversation_thread
