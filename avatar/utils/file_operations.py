import os
import logging
from typing import Optional, Dict, Any
from datetime import datetime, timedelta
from .constants import LOGS_DIRECTORY, TERMINAL_COMMANDS_FILE

def setup_logger() -> logging.Logger:
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    current_date = datetime.now().strftime("%Y-%m-%d")
    log_file = os.path.join(LOGS_DIRECTORY, f"{current_date}.log")
    
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(logging.Formatter('%(asctime)s - %(message)s'))
    
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.ERROR)
    console_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
    
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger

def read_file_content(file_path):
    if not file_path or not os.path.exists(file_path):
        return None
    if os.path.isdir(file_path):
        return f"Directory contents of {file_path}:\n" + "\n".join(os.listdir(file_path))
    try:
        with open(file_path, 'r') as file:
            return file.read()
    except Exception as e:
        logger.error(f"Error reading file: {e}")
        return None

def check_write_permissions(file_path: str) -> bool:
    dir_path = os.path.dirname(file_path)
    if os.path.exists(dir_path):
        return os.access(dir_path, os.W_OK)
    return os.access(os.path.dirname(dir_path), os.W_OK)


def write_to_file(file_path: str, content: str, encoding: str = 'utf-8') -> None:
    try:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'w', encoding=encoding) as file:
            file.write(content)
        logger.info(f"Successfully wrote to file: {file_path}")
    except IOError as e:
        logger.error(f"IOError while writing to file {file_path}: {str(e)}")
        logger.error(traceback.format_exc())
    except Exception as e:
        logger.error(
            f"Unexpected error while writing to file {file_path}: {str(e)}")
        logger.error(traceback.format_exc())

    try:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'w') as file:
            file.write(content)
        logger.info(f"Content successfully written to {file_path}")
        
        # Verify file contents
        with open(file_path, 'r') as file:
            written_content = file.read()
        if written_content == content:
            logger.info(f"File contents verified for {file_path}")
        else:
            logger.warning(f"File contents do not match expected content for {file_path}")
    except PermissionError:
        logger.error(f"Permission denied when writing to file: {file_path}")
    except IOError as e:
        logger.error(f"IO error occurred when writing to file: {file_path}, {e}")
    except Exception as e:
        logger.error(f"Unexpected error writing to file: {file_path}, {e}")

def append_to_file(file_path: str, content: str) -> None:
    try:
        with open(file_path, 'a') as file:
            file.write(content + '\n')
    except Exception as e:
        logger.error(f"Error appending to file {file_path}: {e}")

def write_terminal_command(command: str) -> None:
    append_to_file(TERMINAL_COMMANDS_FILE, command)

from datetime import datetime, timedelta

def read_recent_logs(minutes: int = 15) -> str:
    logs = ""
    fifteen_minutes_ago = datetime.now() - timedelta(minutes=minutes)
    for log_file in sorted(os.listdir(LOGS_DIRECTORY), reverse=True):
        log_file_path = os.path.join(LOGS_DIRECTORY, log_file)
        log_file_datetime = datetime.fromtimestamp(os.path.getmtime(log_file_path))
        if log_file_datetime >= fifteen_minutes_ago:
            logs += read_file_content(log_file_path) or ""
    return logs

def get_directory_tree(root_dir):
    """
    Returns a dictionary representing the directory tree structure with all files.
    """
    directory = {}
    
    # Fetch the contents of the root directory
    filenames = os.listdir(root_dir)
    
    # Iterate over the contents
    for item in filenames:
        path = os.path.join(root_dir, item)
        if os.path.isdir(path):
            # If the item is a directory, recursively call the function
            directory[item] = get_directory_tree(path)
        else:
            # If the item is a file, add it to the dictionary
            directory[item] = None
            
    return directory

logger = setup_logger()