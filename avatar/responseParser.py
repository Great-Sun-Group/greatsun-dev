import shutil
import logging
from utils import read_file, write_file
import os
import re

logger = logging.getLogger(__name__)


def parse_llm_response(llm_response):
    conversation = read_file("avatar/avatarConversation.txt")
    file_operation_performed = False
    processed_response = []

    logger.info("Starting to process LLM response")
    logger.debug(f"Raw LLM response:\n{llm_response}")

    # Define regex patterns for each command
    command_patterns = {
        'read_file': r'read_file/(.+)',
        'write_file': r'write_file/(.+)',
        'list_directory': r'list_directory/(.+)',
        'delete_file': r'delete_file/(.+)',
        'rename_file': r'rename_file/(.+)\nrename_file/(.+)',
        'move_file': r'move_file/(.+)\nmove_file/(.+)'
    }

    lines = llm_response.split('\n')
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        logger.debug(f"Processing line: {line}")


        command_executed = False
        for cmd, pattern in command_patterns.items():
            match = re.match(pattern, line)
            if match:
                try:
                    if cmd == 'read_file':
                        file_path = match.group(1)
                        content = read_file(file_path)
                        processed_response.append(
                            f"Content of {file_path}:\n{content}")
                        file_operation_performed = True
                        command_executed = True

                    elif cmd == 'write_file':
                        file_path = match.group(1)
                        content = '\n'.join(lines[i+1:])
                        end_index = content.find(
                            '[Content ends before the next operation or end of message]')
                        if end_index != -1:
                            content = content[:end_index].strip()
                        write_file(file_path, content)
                        processed_response.append(f"File written: {file_path}")
                        file_operation_performed = True
                        command_executed = True
                        i += content.count('\n') + 1  # Skip content lines

                    elif cmd == 'list_directory':
                        dir_path = match.group(1)
                        dir_contents = os.listdir(dir_path)
                        processed_response.append(
                            f"Contents of {dir_path}:\n{', '.join(dir_contents)}")
                        file_operation_performed = True
                        command_executed = True

                    elif cmd == 'delete_file':
                        file_path = match.group(1)
                        os.remove(file_path)
                        processed_response.append(f"File deleted: {file_path}")
                        file_operation_performed = True
                        command_executed = True

                    elif cmd == 'rename_file':
                        old_path, new_path = match.group(1), match.group(2)
                        os.rename(old_path, new_path)
                        processed_response.append(
                            f"File renamed from {old_path} to {new_path}")
                        file_operation_performed = True
                        command_executed = True
                        i += 1  # Skip the next line as it's part of the rename command

                    elif cmd == 'move_file':
                        src_path, dest_path = match.group(1), match.group(2)
                        shutil.move(src_path, dest_path)
                        processed_response.append(
                            f"File moved from {src_path} to {dest_path}")
                        file_operation_performed = True
                        command_executed = True
                        i += 1  # Skip the next line as it's part of the move command

                except Exception as e:
                    error_msg = f"Error performing {cmd}: {str(e)}"
                    logger.error(error_msg)
                    processed_response.append(error_msg)

                break  # Exit the inner loop after processing a command

        if not command_executed:
            processed_response.append(line)

        i += 1

    processed_response = '\n'.join(processed_response)
    write_file("avatar/avatarConversation.txt", conversation + "\n\n" + processed_response)

    logger.info(f"File operation performed: {file_operation_performed}")
    logger.debug(f"Processed response:\n{processed_response}")

    return processed_response, file_operation_performed