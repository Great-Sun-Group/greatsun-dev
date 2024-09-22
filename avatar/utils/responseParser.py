import os
from pathlib import Path
import json
import re
from typing import Tuple, Dict, Any
from collections import deque
import time

# Assuming BASE_DIR is defined in constants.py
from constants import BASE_DIR


class FileOperation:
    def __init__(self, operation: str, *args: str):
        self.operation = operation
        self.args = args
        self.dependencies = set()


class FileOperationQueue:
    def __init__(self):
        self.queue = deque()
        self.results: Dict[FileOperation, Any] = {}

    def add_operation(self, operation: str, *args: str) -> FileOperation:
        op = FileOperation(operation, *args)
        self.queue.append(op)
        return op

    def add_dependency(self, operation: FileOperation, dependency: FileOperation) -> None:
        operation.dependencies.add(dependency)

    def process_queue(self, conversation_thread: str) -> Tuple[Dict[FileOperation, Any], str]:
        while self.queue:
            op = self.queue.popleft()
            if all(dep in self.results for dep in op.dependencies):
                result = perform_file_operation(op.operation, *op.args)
                self.results[op] = result
                conversation_thread += f"Operation: {
                    op.operation}\nArguments: {op.args}\nResult: {result}\n\n"
                time.sleep(0.1)  # Small delay to allow file system to update
            else:
                self.queue.append(op)
        return self.results, conversation_thread


def parse_llm_response(llm_response: str, conversation_thread: str) -> Tuple[bool, str]:
    file_op_queue = FileOperationQueue()
    file_operation_performed = False
    patterns = {
        'read': r'<read\s+path=(?:")?([^">]+)(?:")?\s*/>',
        'write': r'<write\s+path=(?:")?([^">]+)(?:")?>\s*([\s\S]*?)\s*</write>',
        'append': r'<append\s+path=(?:")?([^">]+)(?:")?>\s*([\s\S]*?)\s*</append>',
        'delete': r'<delete\s+path=(?:")?([^">]+)(?:")?\s*/>',
        'rename': r'<rename\s+current_path=(?:")?([^">]+)(?:")?(?:\s+new_path=(?:")?([^">]+)(?:")?)?\s*/>',
        'move': r'<move\s+current_path=(?:")?([^">]+)(?:")?(?:\s+new_path=(?:")?([^">]+)(?:")?)?\s*/>',
        'list_directory': r'<list_directory\s+path=(?:")?([^">]+)(?:")?\s*/>',
        'create_directory': r'<create_directory\s+path=(?:")?([^">]+)(?:")?\s*/>'
    }

    try:
        for op, pattern in patterns.items():
            matches = re.findall(pattern, llm_response)
            for match in matches:
                if op in ['write', 'append']:
                    path = BASE_DIR / match[0]
                    file_op_queue.add_operation(op, str(path), match[1])
                elif op in ['rename', 'move']:
                    current_path = BASE_DIR / match[0]
                    new_path = BASE_DIR / match[1] if match[1] else None
                    file_op_queue.add_operation(
                        op, str(current_path), str(new_path) if new_path else None)
                else:
                    path = BASE_DIR / match[0]
                    file_op_queue.add_operation(op, str(path))


        results, conversation_thread = file_op_queue.process_queue(conversation_thread)

        # Update conversation_thread with file operation results
        for op, result in results.items():
            if result:
                file_operation_performed = True
                conversation_thread += f"Operation: {op.operation}\n"
                conversation_thread += f"Arguments: {op.args}\n"
                conversation_thread += f"Result: {result}\n\n"

        conversation_thread += "\n\n*** REPLY WITH ANOTHER FILE OPERATION TO RECEIVE AN AUTOMATED RESPONSE, OR RESPOND WITHOUT A FILE OPERATION TO WAIT FOR DEVELOPER RESPONSE ***\n\n"

        # Determine if developer input is required
        developer_input_required = not file_operation_performed

    except Exception as e:
        print(f"Error in parse_llm_response: {str(e)}")
        conversation_thread += f"\nError occurred while parsing LLM response: {str(e)}\n"
        developer_input_required = True

    return developer_input_required, conversation_thread

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

def perform_file_operation(operation: str, *args: str) -> str:
    """
    Perform various file operations with error handling and retries.
    """
    max_attempts = 3
    delay = 0.1
    conversation_thread = []

    for attempt in range(max_attempts):
        try:
            if not validate_file_operation(operation, *args):
                return "Operation not allowed: Invalid path"

            if operation == 'read':
                content = read_file(args[0])
                conversation_thread.append(f"Read file: {args[0]}\nContents: {content}")
            elif operation == 'write':
                success = write_file(args[0], args[1])
                conversation_thread.append(f"Write to file: {args[0]}\nSuccess: {success}")
            elif operation == 'append':
                with open(args[0], 'a') as f:
                    f.write(args[1])
                conversation_thread.append(f"Append to file: {args[0]}\nAppended content: {args[1]}")
            elif operation == 'delete':
                Path(args[0]).unlink()
                conversation_thread.append(f"Delete file: {args[0]}\nSuccess: True")
            elif operation in ['rename', 'move']:
                Path(args[0]).rename(args[1])
                conversation_thread.append(f"{operation.capitalize()} file from {args[0]} to {args[1]}\nSuccess: True")
            elif operation == 'list_directory':
                directory_contents = list(Path(args[0]).iterdir())
                conversation_thread.append(f"List directory: {args[0]}\nContents: {directory_contents}")
            elif operation == 'create_directory':
                Path(args[0]).mkdir(parents=True, exist_ok=True)
                conversation_thread.append(f"Create directory: {args[0]}\nSuccess: True")
            else:
                raise ValueError(f"Unknown operation: {operation}")

            return '\n'.join(conversation_thread)
        except Exception as e:
            if attempt < max_attempts - 1:
                time.sleep(delay)
                delay *= 2  # Exponential backoff
            else:
                error_message = f"Error performing {operation} on {args}: {str(e)}"
                print(error_message)
                conversation_thread.append(error_message)
                return '\n'.join(conversation_thread)

    # This line should never be reached, but it's here for completeness
    return '\n'.join(conversation_thread)

def read_file(file_path: str) -> str:
    """
    Read and return contents of a file, with error handling.
    """
    try:
        with open(file_path, 'r') as file:
            return file.read()
    except FileNotFoundError:
        return f"File not found: {file_path}"
    except Exception as e:
        return f"Error reading file: {str(e)}"

def write_file(file_path: str, file_content: str) -> bool:
    """
    Create the file if it doesn't exist and write over what is there if it does exist,
    with error handling.
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

def get_directory_tree(path: Path) -> Dict[str, Any]:
    """
    Recursively get the directory structure as a dictionary, excluding unnecessary files and directories.
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

def load_initial_context() -> str:
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
        f"\n\n*** MESSAGE FROM DEVELOPER @{os.environ.get('GH_USERNAME')} ***\n\n",
    ]
    return ''.join(initial_context)

# Main execution
if __name__ == "__main__":
    # Example usage
    initial_context = load_initial_context()
    print("Initial context loaded.")
    
    # Example LLM response
    llm_response = "<read path='README.md' />"
    developer_input_required, conversation_thread = parse_llm_response(llm_response, "")
    
    print(f"Developer input required: {developer_input_required}")
    print("Conversation thread:")
    print(conversation_thread)