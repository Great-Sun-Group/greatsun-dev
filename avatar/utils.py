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

async def write_file(file_path, file_content, max_attempts=10, delay=0.1):
    """
    Async function that will create the file if it doesn't exist and write over what is there if it does exist,
    with solid error handling and a confirmation step to ensure the file is readable after writing.

    Args:
    file_path (str): Path to the file to be written
    file_content (str): Content to be written to the file
    max_attempts (int): Maximum number of attempts to confirm file readability
    delay (float): Delay in seconds between confirmation attempts

    Returns:
    bool: True if write operation was successful and file is readable, False otherwise
    """
    try:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        async with aiofiles.open(file_path, 'w') as file:
            await file.write(file_content)
        
        # Confirmation step
        for attempt in range(max_attempts):
            try:
                async with aiofiles.open(file_path, 'r') as file:
                    await file.read(1)  # Try to read at least one byte
                logging.info(f"Successfully wrote to file and confirmed readability: {file_path}")
                return True
            except FileNotFoundError:
                if attempt < max_attempts - 1:
                    await asyncio.sleep(delay)
                else:
                    logging.error(f"File {file_path} not readable after {max_attempts} attempts")
                    return False
    except Exception as e:
        logging.error(f"Error writing to file {file_path}: {str(e)}")
        return False

async def get_directory_tree(path):
    """
    Recursively get the directory structure as a dictionary, excluding irrelevant files and folders.
    This function is asynchronous to avoid blocking the event loop during I/O operations.

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
                subtree = await get_directory_tree(entry.path)
                if subtree:  # Only add non-empty directories
                    tree[entry.name] = subtree
            elif entry.is_file():
                # Check if the file should be included
                if not any(entry.name.endswith(ext) for ext in excluded_files):
                    # Include only relevant file types
                    if entry.name.endswith(('.py', '.ts', '.js', '.json', '.yml', '.yaml', '.md', '.txt')):
                        tree[entry.name] = None
            
            # Yield control to the event loop periodically
            await asyncio.sleep(0)
    except Exception as e:
        logging.error(f"Error getting directory tree for {path}: {str(e)}")

    return tree
