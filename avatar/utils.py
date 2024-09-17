import os
import logging

def read_file(file_path):
    """
    Robust function to read and return contents of a file, with solid error handling.
    If passed the path to a directory, it checks that it is a directory, logs that, and returns a message.

    Args:
    file_path (str): Path to the file or directory to be read

    Returns:
    str: Contents of the file or a message indicating it's a directory
    """
    try:
        if os.path.isdir(file_path):
            logging.info(f"Attempted to read directory: {file_path}")
            return f"The provided path is a directory: {file_path}"

        with open(file_path, 'r') as file:
            content = file.read()
        logging.info(f"Successfully read file: {file_path}")
        return content
    except FileNotFoundError:
        logging.error(f"File not found: {file_path}")
        return f"File not found: {file_path}"
    except Exception as e:
        logging.error(f"Error reading file {file_path}: {str(e)}")
        return f"Error reading file: {str(e)}"


def write_file(file_path, file_content):
    """
    Robust function that will create the file if it doesn't exist and write over what is there if it does exist,
    with solid error handling.

    Args:
    file_path (str): Path to the file to be written
    file_content (str): Content to be written to the file

    Returns:
    bool: True if write operation was successful, False otherwise
    """
    try:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'w') as file:
            file.write(file_content)
        logging.info(f"Successfully wrote to file: {file_path}")
        return True
    except Exception as e:
        logging.error(f"Error writing to file {file_path}: {str(e)}")
        return False


def get_directory_tree(path):
    """
    Recursively get the directory structure as a dictionary, excluding irrelevant files and folders.

    Args:
    path (str): Path to the directory

    Returns:
    dict: Directory structure
    """
    tree = {}
    excluded_dirs = {'node_modules', '__pycache__',
                     '.git', '.vscode', 'venv', 'env', 'build', 'dist'}
    excluded_files = {'.DS_Store', 'Thumbs.db',
                      '*.pyc', '*.pyo', '*.pyd', '*.log'}

    try:
        for entry in os.scandir(path):
            if entry.is_dir() and entry.name not in excluded_dirs:
                subtree = get_directory_tree(entry.path)
                if subtree:  # Only add non-empty directories
                    tree[entry.name] = subtree
            elif entry.is_file():
                # Check if the file should be included
                if not any(entry.name.endswith(ext) for ext in excluded_files):
                    # Include only relevant file types
                    if entry.name.endswith(('.py', '.ts', '.js', '.json', '.yml', '.yaml', '.md', '.txt')):
                        tree[entry.name] = None
    except Exception as e:
        logging.error(f"Error getting directory tree for {path}: {str(e)}")

    return tree


logger = logging.getLogger(__name__)


logger = logging.getLogger(__name__)


logger = logging.getLogger(__name__)


def process_llm_response(llm_response):
    conversation = read_file("avatar/avatarConversation.txt")
    file_operation_performed = False
    processed_response = []

    logger.info("Starting to process LLM response")
    logger.debug(f"Raw LLM response:\n{llm_response}")

    lines = llm_response.split('\n')
    for line in lines:
        line = line.strip()
        logger.debug(f"Processing line: {line}")

        if line.startswith(('/workspaces/', 'read_file/', 'write_file/', 'list_directory/')) or line.startswith('/'):
            parts = line.split('/', 1)
            command = parts[0] if not line.startswith('/') else 'read_file'
            path = '/' + parts[1] if line.startswith('/') else parts[1]

            if command == 'read_file' or line.startswith('/'):
                logger.info(f"Detected file read request: {path}")
                try:
                    read_data = read_file(path)
                    conversation += f"\n\nREAD_FILE\n{path}\n{read_data}"
                    logger.info(f"Successfully read file: {path}")
                    processed_response.append(
                        f"Content of {path}:\n{read_data}")
                    file_operation_performed = True
                except FileNotFoundError:
                    error_msg = f"File not found: {path}"
                    logger.error(error_msg)
                    processed_response.append(error_msg)
                except Exception as e:
                    error_msg = f"Failed to read file {path}: {str(e)}"
                    logger.error(error_msg)
                    processed_response.append(error_msg)

            elif command == 'list_directory':
                logger.info(f"Detected directory list request: {path}")
                try:
                    dir_contents = os.listdir(path)
                    dir_info = f"Contents of {path}:\n" + \
                        "\n".join(dir_contents)
                    conversation += f"\n\nLIST_DIRECTORY\n{path}\n{dir_info}"
                    logger.info(f"Successfully listed directory: {path}")
                    processed_response.append(dir_info)
                    file_operation_performed = True
                except FileNotFoundError:
                    error_msg = f"Directory not found: {path}"
                    logger.error(error_msg)
                    processed_response.append(error_msg)
                except Exception as e:
                    error_msg = f"Failed to list directory {path}: {str(e)}"
                    logger.error(error_msg)
                    processed_response.append(error_msg)

            # Add a blank line after each file operation
            processed_response.append("")
        else:
            processed_response.append(line)

    processed_response = '\n'.join(processed_response)
    write_file("avatar/avatarConversation.txt", conversation)

    logger.info(f"File operation performed: {file_operation_performed}")
    logger.debug(f"Processed response:\n{processed_response}")

    return processed_response, file_operation_performed
