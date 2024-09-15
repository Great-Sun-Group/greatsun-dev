import os
import json
import logging
from typing import Optional, Dict, Any, List
from datetime import datetime, timedelta

# Constants
LOGS_DIRECTORY = "avatar/context/conversationLog"
SUMMARY_FILE = os.path.join("avatar", "context", "context_summary.json")
CONTEXT_DIR = "avatar/context"

# Ensure directories exist
os.makedirs(LOGS_DIRECTORY, exist_ok=True)
os.makedirs(CONTEXT_DIR, exist_ok=True)

def setup_logger() -> logging.Logger:
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    current_date = datetime.now().strftime("%Y-%m-%d")
    log_file = f"{LOGS_DIRECTORY}/{current_date}.log"
    
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(logging.Formatter('%(asctime)s - %(message)s'))
    
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.ERROR)
    console_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
    
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger

logger = setup_logger()

def read_file_content(file_path: str) -> Optional[str]:
    try:
        with open(file_path, 'r') as file:
            return file.read()
    except FileNotFoundError:
        logger.error(f"File not found: {file_path}")
    except Exception as e:
        logger.error(f"Error reading file: {e}")
    return None

def write_to_file(file_path: str, content: str) -> None:
    try:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'w') as file:
            file.write(content)
        logger.info(f"Content written to {file_path}")
    except Exception as e:
        logger.error(f"Error writing to file: {file_path}, {e}")

def read_recent_logs(minutes: int = 15) -> str:
    logs = ""
    fifteen_minutes_ago = datetime.now() - timedelta(minutes=minutes)
    for log_file in sorted(os.listdir(LOGS_DIRECTORY)):
        log_file_path = os.path.join(LOGS_DIRECTORY, log_file)
        log_file_datetime = datetime.strptime(log_file.split('.')[0], "%Y-%m-%d")
        if log_file_datetime >= fifteen_minutes_ago:
            logs += read_file_content(log_file_path) or ""
    return logs

def write_summary_of_context(summary: List[Dict[str, str]]) -> None:
    try:
        with open(SUMMARY_FILE, 'w') as file:
            json.dump(summary, file, indent=2)
        logger.info("Summary of context updated")
    except Exception as e:
        logger.error(f"Error writing summary of context: {e}")

def get_directory_tree(root_dir: str) -> Dict[str, Any]:
    try:
        return {item: get_directory_tree(os.path.join(root_dir, item)) if os.path.isdir(os.path.join(root_dir, item)) else None
                for item in os.listdir(root_dir)}
    except Exception as e:
        logger.error(f"Error getting directory tree: {e}")
        return {}
