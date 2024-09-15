import os
import json
import logging
from typing import Optional, Dict, Any, List
import re
from datetime import datetime, timedelta

# Constants
LOGS_DIRECTORY = "avatar/logs"
CONTEXT_DIR = "avatar/context"
SUMMARY_FILE = os.path.join(CONTEXT_DIR, "context_summary.json")

# Ensure directories exist
os.makedirs(LOGS_DIRECTORY, exist_ok=True)
os.makedirs(CONTEXT_DIR, exist_ok=True)

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

def read_summary_of_context() -> List[Dict[str, str]]:
    try:
        with open(SUMMARY_FILE, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        logger.info("Summary of context file not found, creating an empty file")
        write_summary_of_context([])
        return []
    except Exception as e:
        logger.error(f"Error reading summary of context: {e}")
        return []

def write_summary_of_context(summary: List[Dict[str, Any]]) -> None:
    try:
        with open(SUMMARY_FILE, 'w') as file:
            json.dump(summary, file, indent=2)
        logger.info("Summary of context updated")
    except Exception as e:
        logger.error(f"Error writing summary of context: {e}")

def read_recent_logs(minutes: int = 15) -> str:
    logs = ""
    fifteen_minutes_ago = datetime.now() - timedelta(minutes=minutes)
    for log_file in sorted(os.listdir(LOGS_DIRECTORY), reverse=True):
        log_file_path = os.path.join(LOGS_DIRECTORY, log_file)
        log_file_datetime = datetime.fromtimestamp(os.path.getmtime(log_file_path))
        if log_file_datetime >= fifteen_minutes_ago:
            logs += read_file_content(log_file_path) or ""
    return logs

def get_directory_tree(root_dir: str) -> Dict[str, Any]:
    try:
        return {item: get_directory_tree(os.path.join(root_dir, item)) if os.path.isdir(os.path.join(root_dir, item)) else None
                for item in os.listdir(root_dir)}
    except Exception as e:
        logger.error(f"Error getting directory tree: {e}")
        return {}

def extract_json_from_response(response: str) -> tuple[Optional[dict], str]:
    json_match = re.search(r'```json\n(.*?)\n```', response, re.DOTALL)
    if json_match:
        try:
            json_data = json.loads(json_match.group(1))
            remaining_text = response[:json_match.start()] + response[json_match.end():]
            return json_data, remaining_text.strip()
        except json.JSONDecodeError:
            logger.error("Failed to parse JSON from response")
    return None, response