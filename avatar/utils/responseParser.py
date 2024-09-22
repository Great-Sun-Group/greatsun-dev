import os
import re
import json
from pathlib import Path
from typing import Tuple, Dict, Any
import shutil

BASE_DIR = Path('/workspaces/greatsun-dev')


def parse_llm_response(llm_response: str, conversation_thread: str) -> Tuple[bool, str]:
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

    file_operation_performed = False

    for op, pattern in patterns.items():
        matches = re.findall(pattern, llm_response)
        for match in matches:
            file_operation_performed = True
            if op in ['read', 'delete', 'list_directory', 'create_directory']:
                path = match if isinstance(match, str) else match[0]
                result = perform_file_operation(op, path)
            elif op in ['write', 'append']:
                path, content = match
                result = perform_file_operation(op, path, content)
            elif op in ['rename', 'move']:
                current_path, new_path = match
                result = perform_file_operation(
                    op, current_path, new_path=new_path)
            conversation_thread += f"Operation: {
                op}\nArguments: {match}\nResult: {result}\n\n"

    return not file_operation_performed, conversation_thread


def perform_file_operation(operation: str, path: str, content: str = None, new_path: str = None) -> str:
    # If the path is absolute, use it as is. Otherwise, make it relative to BASE_DIR
    full_path = Path(path) if Path(path).is_absolute() else BASE_DIR / path

    try:
        if operation == 'read':
            with open(full_path, 'r') as file:
                return f"File contents:\n{file.read()}"

        elif operation == 'write':
            full_path.parent.mkdir(parents=True, exist_ok=True)
            with open(full_path, 'w') as file:
                file.write(content)
            return f"File written successfully: {full_path}"

        elif operation == 'append':
            with open(full_path, 'a') as file:
                file.write(content)
            return f"Content appended successfully to: {full_path}"


        elif operation == 'delete':
            if full_path.is_file():
                os.remove(full_path)
                return f"File deleted successfully: {full_path}"
            elif full_path.is_dir():
                shutil.rmtree(full_path)
                return f"Directory deleted successfully: {full_path}"
            else:
                return f"Path not found: {full_path}"

        elif operation == 'rename' or operation == 'move':
            new_full_path = Path(new_path) if Path(new_path).is_absolute() else BASE_DIR / new_path
            new_full_path.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(full_path, new_full_path)
            return f"{'Renamed' if operation == 'rename' else 'Moved'} successfully: {full_path} -> {new_full_path}"
        
        elif operation == 'list_directory':
            if full_path.is_dir():
                return f"Directory contents of {full_path}:\n" + "\n".join(str(item) for item in full_path.iterdir())
            else:
                return f"Not a directory: {full_path}"
        
        elif operation == 'create_directory':
            full_path.mkdir(parents=True, exist_ok=True)
            return f"Directory created successfully: {full_path}"
        
        else:
            return f"Unknown operation: {operation}"

    except Exception as e:
        return f"Error performing {operation} on {path}: {str(e)}"

def get_directory_tree(path: Path) -> Dict[str, Any]:
    tree = {}
    excluded_files = {'.DS_Store', 'Thumbs.db', '.gitignore', '.gitattributes', '.env', '.coverage',
        '*.pyc', '*.pyo', '*.whl', '*.egg', '*.log', '*.zip', '*.tar.gz', '*.rar', '*.db', '*.sqlite'}
    excluded_dirs = {'__pycache__', '.git', '.svn', '.hg', 'node_modules', 'venv',
        'env', 'build', 'dist', '.vscode', '.idea', 'tmp', 'temp', 'htmlcov'}

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
        f"\n\n*** MESSAGE FROM DEVELOPER @{
            os.environ.get('GH_USERNAME')} ***\n\n",
    ]
    return ''.join(initial_context)


def read_file(file_path: Path) -> str:
    try:
        return file_path.read_text()
    except FileNotFoundError:
        return f"File not found: {file_path}"
    except Exception as e:
        return f"Error reading file: {str(e)}"


def write_file(file_path: Path, file_content: str) -> bool:
    try:
        file_path.parent.mkdir(parents=True, exist_ok=True)
        with file_path.open('w') as file:
            file.write(file_content)
        return True
    except Exception as e:
        print(f"Error writing to file {file_path}: {str(e)}")
        return False
