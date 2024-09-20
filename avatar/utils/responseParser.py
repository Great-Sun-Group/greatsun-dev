import re
import os
import logging
from typing import Tuple, List
from utils.file_operations import FileOperationQueue, FileOperation

logger = logging.getLogger(__name__)


def parse_llm_response(conversation_thread: str, llm_response: str) -> Tuple[str, bool, str]:
    file_op_queue = FileOperationQueue()
    file_operation_performed = False
    processed_response = []
    terminal_output = []

    logger.info("Starting to process LLM response")
    logger.debug(f"Raw LLM response:\n{llm_response}")

    patterns = {
        'read': r'<read path=(?:")?([^">]+)(?:")? />',
        'write': r'<write path=(?:")?([^">]+)(?:")?>\s*([\s\S]*?)\s*</write>',
        'append': r'<append path=(?:")?([^">]+)(?:")?>([\s\S]*?)</append>',
        'delete': r'<delete path=(?:")?([^">]+)(?:")? />',
        'rename': r'<rename current_path=(?:")?([^">]+)(?:")? new_path=(?:")?([^">]+)(?:")? />',
        'move': r'<move current_path=(?:")?([^">]+)(?:")? new_path=(?:")?([^">]+)(?:")? />',
        'list_directory': r'<list_directory path=(?:")?([^">]+)(?:")? />',
        'create_directory': r'<create_directory path=(?:")?([^">]+)(?:")? />'
    }

    # Process file operations
    for operation, pattern in patterns.items():
        llm_response = process_operation(
            pattern, operation, file_op_queue, terminal_output, llm_response)

    # Process all queued operations
    results = file_op_queue.process_queue()

    for op, result in results.items():
        if result is not False:
            file_operation_performed = True
            if op.operation == 'read':
                conversation_thread += f"\n\nContent of {
                    op.args[0]}:\n{result}"
            else:
                processed_response.append(format_operation_result(op, result))

    # Save action results to conversation thread
    processed_response = '\n'.join(processed_response)
    conversation_thread += f"\n\n*** LLM RESPONSE ***\n\n{
        llm_response}\n\n*** PROCESSED RESPONSE ***\n\n{processed_response}"

    # Add the modified LLM response (with placeholders) to terminal output
    terminal_output.append(llm_response)

    # Prepare terminal output
    terminal_output = '\n'.join(terminal_output)

    logger.info(f"File operation performed: {file_operation_performed}")
    logger.debug(f"Processed response:\n{processed_response}")
    logger.debug(f"Terminal output:\n{terminal_output}")

    return conversation_thread, file_operation_performed, terminal_output

def process_operation(pattern: str, operation: str, file_op_queue: FileOperationQueue,
                      terminal_output: List[str], llm_response: str) -> str:
    def replace_func(match):
        if operation == 'read':
            path = os.path.abspath(match.group(1))
            read_op = file_op_queue.add_operation('read', path)
            for op in file_op_queue.queue:
                if op.operation in ['write', 'append'] and op.args[0] == path:
                    file_op_queue.add_dependency(read_op, op)
            terminal_output.append(f"Reading file: {path}")
            return f"<read path=\"{path}\" />"
        elif operation == 'write':
            path, content = match.groups()
            path = os.path.abspath(path)
            file_op_queue.add_operation('write', path, content)
            terminal_output.append(f"File written: {path}")
            return f"<write path=\"{path}\">{content}</write>"
        elif operation == 'append':
            path, content = match.groups()
            path = os.path.abspath(path)
            file_op_queue.add_operation('append', path, content)
            terminal_output.append(f"Content appended to: {path}")
            return f"<append path=\"{path}\">{content}</append>"
        elif operation == 'delete':
            path = os.path.abspath(match.group(1))
            file_op_queue.add_operation('delete', path)
            terminal_output.append(f"File deleted: {path}")
            return f"<delete path=\"{path}\" />"
        elif operation in ['rename', 'move']:
            current_path, new_path = match.groups()
            current_path = os.path.abspath(current_path)
            new_path = os.path.abspath(new_path)
            file_op_queue.add_operation(operation, current_path, new_path)
            terminal_output.append(f"File {operation}d from {current_path} to {new_path}")
            return f"<{operation} current_path=\"{current_path}\" new_path=\"{new_path}\" />"
        elif operation == 'list_directory':
            path = os.path.abspath(match.group(1))
            file_op_queue.add_operation('list_directory', path)
            terminal_output.append(f"Listing directory: {path}")
            return f"<list_directory path=\"{path}\" />"
        elif operation == 'create_directory':
            path = os.path.abspath(match.group(1))
            file_op_queue.add_operation('create_directory', path)
            terminal_output.append(f"Directory created: {path}")
            return f"<create_directory path=\"{path}\" />"
        else:
            return match.group(0)

    new_response = re.sub(pattern, replace_func, llm_response)
    return new_response


def format_operation_result(op: FileOperation, result: str) -> str:
    if op.operation == 'read':
        return f"Content of {op.args[0]}:\n{result}"
    elif op.operation == 'write':
        return f"File written: {op.args[0]}\nContent:\n{op.args[1]}"
    elif op.operation == 'append':
        return f"Content appended to: {op.args[0]}\nAppended content:\n{op.args[1]}"
    elif op.operation == 'delete':
        return f"File deleted: {op.args[0]}"
    elif op.operation in ['rename', 'move']:
        return f"File {op.operation}d from {op.args[0]} to {op.args[1]}"
    elif op.operation == 'list_directory':
        return f"Contents of {op.args[0]}:\n{', '.join(result) if isinstance(result, list) else str(result)}"
    elif op.operation == 'create_directory':
        return f"Directory created: {op.args[0]}"
    else:
        return f"Unknown operation: {op.operation}"


def sanitize_path(path: str) -> str:
    """Sanitize and normalize the given file path."""
    return os.path.normpath(os.path.abspath(path))


def is_path_allowed(path: str) -> bool:
    """Check if the given path is within the allowed directory."""
    allowed_dir = '/workspaces/greatsun-dev'
    return os.path.commonpath([path, allowed_dir]) == allowed_dir


def validate_file_operation(operation: str, path: str, new_path: str = None) -> bool:
    """Validate file operations to ensure they're within allowed directories."""
    path = sanitize_path(path)
    if not is_path_allowed(path):
        logger.warning(
            f"Attempted operation outside allowed directory: {path}")
        return False

    if new_path:
        new_path = sanitize_path(new_path)
        if not is_path_allowed(new_path):
            logger.warning(
                f"Attempted operation outside allowed directory: {new_path}")
            return False

    return True


logger.info("responseParser module initialized")
