import xml.etree.ElementTree as ET
import os
import shutil
import logging
from utils import read_file, write_file
import re

logger = logging.getLogger(__name__)

def parse_llm_response(llm_response):
    conversation = read_file("avatar/avatarConversation.txt")
    file_operation_performed = False
    processed_response = []

    logger.info("Starting to process LLM response")
    logger.debug(f"Raw LLM response:\n{llm_response}")

    # Extract XML content
    xml_match = re.search(r'<response>(.*?)</response>', llm_response, re.DOTALL)
    if not xml_match:
        logger.error("No valid XML found in the response")
        return llm_response, False

    xml_content = f"<response>{xml_match.group(1)}</response>"

    try:
        root = ET.fromstring(xml_content)
    except ET.ParseError as e:
        logger.error(f"Failed to parse XML: {str(e)}")
        return llm_response, False

    # Process file operations
    file_ops_elem = root.find('file_operations')
    if file_ops_elem is not None:
        for operation in file_ops_elem:
            try:
                if operation.tag == 'read':
                    path = operation.get('path')
                    content = read_file(path)
                    processed_response.append(f"Content of {path}:\n{content}")
                    file_operation_performed = True

                elif operation.tag == 'write':
                    path = operation.get('path')
                    content = operation.text
                    write_file(path, content)
                    processed_response.append(f"File written: {path}")
                    file_operation_performed = True

                elif operation.tag == 'append':
                    path = operation.get('path')
                    content = operation.text
                    with open(path, 'a') as f:
                        f.write(content)
                    processed_response.append(f"Content appended to: {path}")
                    file_operation_performed = True

                elif operation.tag == 'delete':
                    path = operation.get('path')
                    os.remove(path)
                    processed_response.append(f"File deleted: {path}")
                    file_operation_performed = True

                elif operation.tag == 'rename':
                    current_path = operation.get('current_path')
                    new_path = operation.get('new_path')
                    os.rename(current_path, new_path)
                    processed_response.append(f"File renamed from {current_path} to {new_path}")
                    file_operation_performed = True

                elif operation.tag == 'move':
                    current_path = operation.get('current_path')
                    new_path = operation.get('new_path')
                    shutil.move(current_path, new_path)
                    processed_response.append(f"File moved from {current_path} to {new_path}")
                    file_operation_performed = True

                elif operation.tag == 'list_directory':
                    path = operation.get('path')
                    dir_contents = os.listdir(path)
                    processed_response.append(f"Contents of {path}:\n{', '.join(dir_contents)}")
                    file_operation_performed = True

                elif operation.tag == 'create_directory':
                    path = operation.get('path')
                    os.makedirs(path, exist_ok=True)
                    processed_response.append(f"Directory created: {path}")
                    file_operation_performed = True

            except Exception as e:
                error_msg = f"Error performing {operation.tag}: {str(e)}"
                logger.error(error_msg)
                processed_response.append(error_msg)

    # Process message to developer
    message_elem = root.find('message_to_developer')
    if message_elem is not None and message_elem.text:
        processed_response.append(f"Message to developer: {message_elem.text}")

    # Prepare response to developer
    response_to_developer = llm_response

    # Remove file contents of written files from the response
    if file_ops_elem is not None:
        for operation in file_ops_elem:
            if operation.tag == 'write':
                path = operation.get('path')
                content = operation.text
                if content:
                    response_to_developer = response_to_developer.replace(content, f"[Content written to {path}]")

    processed_response = '\n'.join(processed_response)
    write_file("avatar/avatarConversation.txt", conversation + "\n\n" + processed_response)

    logger.info(f"File operation performed: {file_operation_performed}")
    logger.debug(f"Processed response:\n{processed_response}")
    logger.debug(f"Response to developer:\n{response_to_developer}")

    return response_to_developer, file_operation_performed