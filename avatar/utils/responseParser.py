import re
from pathlib import Path
from typing import Tuple
from file_operations import FileOperationQueue
from constants import BASE_DIR

def parse_llm_response(llm_response: str, conversation_thread: str) -> Tuple[bool, str]:
    file_op_queue = FileOperationQueue()
    file_operation_performed = False
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

    # Print the llm_response to the terminal, with file contents replaced
    printed_response = llm_response
    for op in ['write', 'append']:
        printed_response = re.sub(
            patterns[op], f'<{op} path="\\1">[file contents here]</{op}>', printed_response)
    print(printed_response)

    # Extract queued operations from llm_response using the patterns above, and process them
    for op, pattern in patterns.items():
        matches = re.findall(pattern, llm_response)
        for match in matches:
            if op in ['write', 'append']:
                file_op_queue.add_operation(
                    op, str(BASE_DIR / match[0]), match[1])
            elif op in ['rename', 'move']:
                file_op_queue.add_operation(
                    op, str(BASE_DIR / match[0]), str(BASE_DIR / match[1]))
            else:
                file_op_queue.add_operation(op, str(BASE_DIR / match[0]))

    results, conversation_thread = file_op_queue.process_queue(
        conversation_thread)

    # Update conversation_thread with file operation results
    for op, result in results.items():
        if result is not False:
            file_operation_performed = True
            conversation_thread += f"Operation: {op.operation}\n"
            conversation_thread += f"Arguments: {op.args}\n"
            conversation_thread += f"Result: {result}\n\n"
    conversation_thread += "\n\n*** REPLY WITH ANOTHER A FILE OPERATION TO RECEIVE AN AUTOMATED RESPONSE, OR RESPOND WITHOUT A FILE OPERATION TO WAIT FOR DEVELOPER RESPONSE ***\n\n"

    # Determine if developer input is required
    developer_input_required = not file_operation_performed

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