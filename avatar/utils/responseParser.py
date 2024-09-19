import re
import os
import logging
from utils.file_operations import FileOperationQueue

logger = logging.getLogger(__name__)

def parse_llm_response(conversation_thread, llm_response):
    file_op_queue = FileOperationQueue()
    file_operation_performed = False
    developer_input_required = False
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
        'create_directory': r'<create_directory path=(?:")?([^">]+)(?:")? />',
        'request_developer_action': r'<request_developer_action=true>'
    }

    for operation, pattern in patterns.items():
        matches = re.finditer(pattern, llm_response, re.DOTALL)
        for match in matches:
            if operation == 'read':
                path = os.path.abspath(match.group(1))
                read_op = file_op_queue.add_operation('read', path)
                for op in file_op_queue.queue:
                    if op.operation in ['write', 'append'] and op.args[0] == path:
                        file_op_queue.add_dependency(read_op, op)
                terminal_output.append(f"Reading file: {path}")
            elif operation == 'write':
                path, content = match.groups()
                path = os.path.abspath(path)
                file_op_queue.add_operation('write', path, content)
                terminal_output.append(f"File written: {path}")
            elif operation == 'append':
                path, content = match.groups()
                path = os.path.abspath(path)
                file_op_queue.add_operation('append', path, content)
                terminal_output.append(f"Content appended to: {path}")
            elif operation == 'delete':
                path = os.path.abspath(match.group(1))
                file_op_queue.add_operation('delete', path)
                terminal_output.append(f"File deleted: {path}")
            elif operation in ['rename', 'move']:
                current_path, new_path = match.groups()
                current_path = os.path.abspath(current_path)
                new_path = os.path.abspath(new_path)
                file_op_queue.add_operation(operation, current_path, new_path)
                terminal_output.append(f"File {operation}d from {current_path} to {new_path}")
            elif operation == 'list_directory':
                path = os.path.abspath(match.group(1))
                file_op_queue.add_operation('list_directory', path)
                terminal_output.append(f"Listing directory: {path}")
            elif operation == 'create_directory':
                path = os.path.abspath(match.group(1))
                file_op_queue.add_operation('create_directory', path)
                terminal_output.append(f"Directory created: {path}")
            elif operation == 'request_developer_action':
                developer_input_required = True
                terminal_output.append("Developer action requested")

    # Process all queued operations
    results = file_op_queue.process_queue()

    for op, result in results.items():
        if op.operation == 'read':
            processed_response.append(f"Content of {op.args[0]}:\n{result}")
        elif op.operation == 'write':
            processed_response.append(f"File written: {op.args[0]}")
        elif op.operation == 'append':
            processed_response.append(f"Content appended to: {op.args[0]}")
        elif op.operation == 'delete':
            processed_response.append(f"File deleted: {op.args[0]}")
        elif op.operation in ['rename', 'move']:
            processed_response.append(f"File {op.operation}d from {op.args[0]} to {op.args[1]}")
        elif op.operation == 'list_directory':
            processed_response.append(f"Contents of {op.args[0]}:\n{', '.join(result) if isinstance(result, list) else str(result)}")
        elif op.operation == 'create_directory':
            processed_response.append(f"Directory created: {op.args[0]}")

        if result is not False:
            file_operation_performed = True

    # Save action results to conversation thread
    processed_response = '\n'.join(processed_response)
    conversation_thread = f"{conversation_thread}\n\n*** OPERATION RESULTS ***\n\n{processed_response}"

    # Prepare terminal output
    terminal_output = '\n'.join(terminal_output)

    # Replace file contents with placeholder for write and append operations in terminal output only
    for operation in ['write', 'append']:
        pattern = rf'({operation.capitalize()}.*?:.*?)(\n|$)'
        terminal_output = re.sub(pattern, r'\1\n[File contents not displayed]\2', terminal_output, flags=re.IGNORECASE)

    # Replace directory contents with placeholder for list_directory operation in terminal output
    pattern = r'(Listing directory:.*?)(\n|$)'
    terminal_output = re.sub(pattern, r'\1\n[Directory contents not displayed]\2', terminal_output, flags=re.IGNORECASE)

    logger.info(f"File operation performed: {file_operation_performed}")
    logger.info(f"Developer input required: {developer_input_required}")
    logger.debug(f"Processed response (full content):\n{processed_response}")
    logger.debug(f"Terminal output (with placeholders):\n{terminal_output}")

    # Return the updated conversation thread (full content), whether developer input is required, and the modified terminal output
    return conversation_thread, developer_input_required, terminal_output