import shutil
import logging

logger = logging.getLogger(__name__)


def parse_llm_response(llm_response):
    conversation = read_file("avatar/avatarConversation.txt")
    file_operation_performed = False
    processed_response = []

    logger.info("Starting to process LLM response")
    logger.debug(f"Raw LLM response:\n{llm_response}")

    lines = llm_response.split('\n')
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        logger.debug(f"Processing line: {line}")

        # Check for various file operation requests
        if line.startswith(('read_file', 'write_file', 'list_directory', 'delete_file', 'rename_file', 'move_file')):
            parts = line.split(None, 2)
            command = parts[0]
            args = parts[1:] if len(parts) > 1 else []

            try:
                if command == 'read_file':
                    file_path = args[0]
                    content = read_file(file_path)
                    processed_response.append(
                        f"Content of {file_path}:\n{content}")
                    file_operation_performed = True

                elif command == 'write_file':
                    file_path = args[0]
                    content = args[1] if len(args) > 1 else lines[i+1]
                    write_file(file_path, content)
                    processed_response.append(f"File written: {file_path}")
                    file_operation_performed = True
                    i += 1  # Skip the next line if it was the content

                elif command == 'list_directory':
                    dir_path = args[0]
                    dir_contents = os.listdir(dir_path)
                    processed_response.append(
                        f"Contents of {dir_path}:\n{', '.join(dir_contents)}")
                    file_operation_performed = True

                elif command == 'delete_file':
                    file_path = args[0]
                    os.remove(file_path)
                    processed_response.append(f"File deleted: {file_path}")
                    file_operation_performed = True

                elif command == 'rename_file':
                    old_path, new_path = args[0], args[1]
                    os.rename(old_path, new_path)
                    processed_response.append(
                        f"File renamed from {old_path} to {new_path}")
                    file_operation_performed = True

                elif command == 'move_file':
                    src_path, dest_path = args[0], args[1]
                    shutil.move(src_path, dest_path)
                    processed_response.append(
                        f"File moved from {src_path} to {dest_path}")
                    file_operation_performed = True

            except Exception as e:
                error_msg = f"Error performing {command}: {str(e)}"
                logger.error(error_msg)
                processed_response.append(error_msg)

        else:
            processed_response.append(line)

        i += 1

    processed_response = '\n'.join(processed_response)
    write_file("avatar/avatarConversation.txt",
               conversation + "\n\n" + processed_response)

    logger.info(f"File operation performed: {file_operation_performed}")
    logger.debug(f"Processed response:\n{processed_response}")

    return processed_response, file_operation_performed
