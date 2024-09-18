import re
import os
import shutil
import logging
from utils import read_file, write_file

logger = logging.getLogger(__name__)

async def parse_llm_response(conversation_thread, llm_response):
    file_operation_performed = False
    developer_input_required = False
    processed_response = []

    logger.info("Starting to process LLM response")
    logger.debug(f"Raw LLM response:\n{llm_response}")

    # Define regex patterns for each operation
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
            try:
                if operation == 'read':
                    path = match.group(1)
                    content = await read_file(path)
                    processed_response.append(f"Content of {path}:\n{content}")
                    file_operation_performed = True

                elif operation == 'write':
                    path, content = match.groups()
                    await write_file(path, content)
                    processed_response.append(f"File written: {path}")
                    file_operation_performed = True

                elif operation == 'append':
                    path, content = match.groups()
                    with open(path, 'a') as f:
                        f.write(content)
                    processed_response.append(f"Content appended to: {path}")
                    file_operation_performed = True

                elif operation == 'delete':
                    path = match.group(1)
                    os.remove(path)
                    processed_response.append(f"File deleted: {path}")
                    file_operation_performed = True

                elif operation == 'rename':
                    current_path, new_path = match.groups()
                    os.rename(current_path, new_path)
                    processed_response.append(f"File renamed from {current_path} to {new_path}")
                    file_operation_performed = True

                elif operation == 'move':
                    current_path, new_path = match.groups()
                    shutil.move(current_path, new_path)
                    processed_response.append(f"File moved from {current_path} to {new_path}")
                    file_operation_performed = True

                elif operation == 'list_directory':
                    path = match.group(1)
                    dir_contents = os.listdir(path)
                    processed_response.append(f"Contents of {path}:\n{', '.join(dir_contents)}")
                    file_operation_performed = True

                elif operation == 'create_directory':
                    path = match.group(1)
                    os.makedirs(path, exist_ok=True)
                    processed_response.append(f"Directory created: {path}")
                    file_operation_performed = True

                elif operation == 'request_developer_action':
                    processed_response.append("Developer action required")
                    developer_input_required = True

            except Exception as e:
                error_msg = f"Error performing {operation}: {str(e)}"
                logger.error(error_msg)
                processed_response.append(error_msg)

    # Save action results to conversation thread
    processed_response = '\n'.join(processed_response)
    conversation_thread = conversation_thread + "\n\n" + processed_response

    if developer_input_required or not file_operation_performed:
        developer_input_required = True

    # Prepare response to developer
    response_to_developer = llm_response

    # Remove file contents of written files from the response
    for match in re.finditer(patterns['write'], llm_response, re.DOTALL):
        path, content = match.groups()
        if content:
            response_to_developer = response_to_developer.replace(content, f"[Content written to {path}]")
            print("\nAvatar:")
            print(response_to_developer)

    logger.info(f"File operation performed: {file_operation_performed}")
    logger.info(f"Developer input required: {developer_input_required}")
    logger.debug(f"Processed response:\n{processed_response}")
    logger.debug(f"Response to developer:\n{response_to_developer}")

    return conversation_thread, developer_input_required