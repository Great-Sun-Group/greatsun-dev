import os
import re
import shutil
from typing import Tuple
from pathlib import Path
from config import BASE_DIR


def llm_response_for_developer(llm_response: str) -> str:
    patterns = {
        'write': r'(<write\s+path=(?:")?[^">]+(?:")?>\s*)([\s\S]*?)(\s*</write>)',
        'append': r'(<append\s+path=(?:")?[^">]+(?:")?>\s*)([\s\S]*?)(\s*</append>)'
    }

    for op, pattern in patterns.items():
        llm_response = re.sub(
            pattern, r'\1[file contents here]\3', llm_response)

    return llm_response


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
            conversation_thread += f"Operation: {op}\nArguments: {match}\nResult: {result}\n\n"
            print(f"Operation: {op}\nResult: {result}\n\n")

    return not file_operation_performed, conversation_thread


def perform_file_operation(operation: str, path: str, content: str = None, new_path: str = None) -> str:
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
        elif operation in ['rename', 'move']:
            new_full_path = Path(new_path) if Path(
                new_path).is_absolute() else BASE_DIR / new_path
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
