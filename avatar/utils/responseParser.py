import re
import os
import logging
from typing import Tuple, List
from utils.file_operations import FileOperationQueue, FileOperation

logger = logging.getLogger(__name__)


def parse_llm_response(conversation_thread: str, llm_response: str) -> Tuple[str, bool, str]:
    file_op_queue = FileOperationQueue()
    file_operation_performed = False
    developer_input_required = False
    processed_response: List[str] = []
    terminal_output: List[str] = []

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
        'create_directory': r'<create_directory path=(?:")?([^">]+)(?:")? />',
        'request_developer_action': r'<request_developer_action=true>'
    }

    # Process file operations
    for operation, pattern in patterns.items():
        llm_response, dev_action = process_operation(
            pattern, operation, file_op_queue, terminal_output, llm_response)
        if dev_action:
            developer_input_required = True

    # Process all queued operations
    results = file_op_queue.process_queue()

    for op, result in results.items():
        if result is not False:
            file_operation_performed = True
            processed_response.append(format_operation_result(op, result))

    # Save action results to conversation thread
    processed_response_str = '\n'.join(processed_response)
    conversation_thread += f"\n\n*** LLM RESPONSE ***\n\n{
        llm_response}\n\n*** PROCESSED RESPONSE ***\n\n{processed_response_str}"

    # Add the modified LLM response (with placeholders) to terminal output
    terminal_output.append(llm_response)

    # Prepare terminal output
    terminal_output_str = '\n'.join(terminal_output)

    logger.info(f"File operation performed: {file_operation_performed}")
    logger.info(f"Developer input required: {developer_input_required}")
    logger.debug(f"Processed response:\n{processed_response_str}")
    logger.debug(f"Terminal output:\n{terminal_output_str}")

    # Return the updated conversation thread, whether developer input is required, and the terminal output
    return conversation_thread, developer_input_required, terminal_output_str


def process_operation(pattern: str, operation: str, file_op_queue: FileOperationQueue, terminal_output: List[str], llm_response: str) -> Tuple[str, bool]:
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
            return f"<write path=\"{path}\">[File contents not displayed]</write>"
        elif operation == 'append':
            path, content = match.groups()
            path = os.path.abspath(path)
            file_op_queue.add_operation('append', path, content)
            terminal_output.append(f"Content appended to: {path}")
            return f"<append path=\"{path}\">[Appended contents not displayed]</append>"
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
            terminal_output.append(f"File {operation}d from {
                                   current_path} to {new_path}")
            return f"<{operation} current_path=\"{current_path}\" new_path=\"{new_path}\" />"
        elif operation == 'list_directory':
            path = os.path.abspath(match.group(1))
            file_op_queue.add_operation('list_directory', path)
            terminal_output.append(f"Listing directory: {path}")
            return f"<list_directory path=\"{path}\">[Directory contents not displayed]</list_directory>"
        elif operation == 'create_directory':
            path = os.path.abspath(match.group(1))
            file_op_queue.add_operation('create_directory', path)
            terminal_output.append(f"Directory created: {path}")
            return f"<create_directory path=\"{path}\" />"
        elif operation == 'request_developer_action':
            terminal_output.append("Developer action requested")
            return "<request_developer_action=true>"
        else:
            return match.group(0)


    new_response = re.sub(pattern, replace_func, llm_response)
    dev_action_requested = operation == 'request_developer_action' and new_response != llm_response
    return new_response, dev_action_requested


def format_operation_result(op: FileOperation, result: any) -> str:
    if op.operation == 'read':
        return f"Content of {op.args[0]}:\n{result}"
    elif op.operation == 'write':
        return f"File written: {op.args[0]}"
    elif op.operation == 'append':
        return f"Content appended to: {op.args[0]}"
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
    allowed_directory = "/workspaces/greatsun-dev"
    return os.path.commonpath([path, allowed_directory]) == allowed_directory


def validate_file_operation(operation: str, path: str, *args) -> bool:
    """Validate file operations to ensure they're safe and allowed."""
    sanitized_path = sanitize_path(path)
    if not is_path_allowed(sanitized_path):
        logger.warning(f"Attempted operation outside allowed directory: {
                       sanitized_path}")
        return False

    if operation in ['read', 'write', 'append']:
        if not os.path.exists(os.path.dirname(sanitized_path)):
            logger.warning(f"Parent directory does not exist for: {
                           sanitized_path}")
            return False
    elif operation in ['delete', 'rename', 'move', 'list_directory']:
        if not os.path.exists(sanitized_path):
            logger.warning(f"Path does not exist: {sanitized_path}")
            return False
    elif operation == 'create_directory':
        if os.path.exists(sanitized_path):
            logger.warning(f"Directory already exists: {sanitized_path}")
            return False

    return True

# Add this function to the FileOperationQueue class in file_operations.py


def add_operation(self, operation: str, *args) -> FileOperation:
    if validate_file_operation(operation, args[0], *args[1:]):
        op = FileOperation(operation, args)
        self.queue.append(op)
        return op
    else:
        logger.warning(f"Invalid file operation: {operation} {args}")
        return None
