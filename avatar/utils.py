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


import os
import logging

def write_file(file_path, file_content, base_path=None):
    """
    Robust function that will create the file if it doesn't exist and write over what is there if it does exist,
    with solid error handling. It transforms absolute paths into relative paths before writing.

    Args:
    file_path (str): Path to the file to be written
    file_content (str): Content to be written to the file
    base_path (str, optional): Base path to use for creating relative paths. If None, the current working directory is used.

    Returns:
    bool: True if write operation was successful, False otherwise
    """
    try:
        # If base_path is not provided, use the current working directory
        if base_path is None:
            base_path = os.getcwd()

        # Convert absolute path to relative path
        relative_path = os.path.relpath(file_path, base_path)

        # Create directory structure if it doesn't exist
        os.makedirs(os.path.dirname(relative_path), exist_ok=True)

        # Write content to the file using the relative path
        with open(relative_path, 'w') as file:
            file.write(file_content)

        logging.info(f"Successfully wrote to file: {relative_path}")
        return True
    except Exception as e:
        logging.error(f"Error writing to file {relative_path}: {str(e)}")
        return False