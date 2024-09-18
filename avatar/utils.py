import os
import logging
import aiofiles

async def read_file(file_path):
    """
    Async function to read and return contents of a file, with solid error handling.
    If passed the path to a directory, it checks that it is a directory, logs that, and returns a message.

    Args:
    file_path (str): Path to the file or directory to be read

    Returns:
    str: Contents of the file or a message indicating it's a directory
    """
    logging.info(f"Attempting to read file: {file_path}")
    try:
        if os.path.isdir(file_path):
            logging.info(f"Attempted to read directory: {file_path}")
            return f"The provided path is a directory: {file_path}"

        async with aiofiles.open(file_path, 'r') as file:
            content = await file.read()
        logging.info(f"Successfully read file: {file_path}")
        return content
    except FileNotFoundError:
        logging.error(f"File not found: {file_path}")
        return f"File not found: {file_path}"
    except Exception as e:
        logging.error(f"Error reading file {file_path}: {str(e)}", exc_info=True)
        return f"Error reading file: {str(e)}"

async def write_file(file_path, file_content):
    """
    Async function that will create the file if it doesn't exist and write over what is there if it does exist,
    with solid error handling.

    Args:
    file_path (str): Path to the file to be written
    file_content (str): Content to be written to the file

    Returns:
    bool: True if write operation was successful, False otherwise
    """
    try:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        async with aiofiles.open(file_path, 'w') as file:
            await file.write(file_content)
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