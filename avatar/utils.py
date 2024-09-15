import os
import logging
from datetime import datetime
import json
import re

def setup_logger(logs_directory: str) -> logging.Logger:
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    current_date = datetime.now().strftime("%Y-%m-%d")
    log_file = f"{logs_directory}/{current_date}.log"
    
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(logging.Formatter('%(asctime)s - %(message)s'))
    
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.ERROR)
    console_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
    
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger

def read_file_content(file_path: str) -> str:
    try:
        with open(file_path, 'r') as file:
            content = file.read()
        return content
    except FileNotFoundError:
        return ''

def write_to_file(file_path: str, content: str) -> None:
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, 'w') as file:
        file.write(content)

def read_recent_logs(logs_directory: str, max_logs: int = 15) -> list[dict]:
    log_files = sorted([f for f in os.listdir(logs_directory) if f.endswith('.log')], reverse=True)
    recent_logs = []
    for log_file in log_files[:max_logs]:
        log_path = os.path.join(logs_directory, log_file)
        with open(log_path, 'r') as file:
            log_content = file.read()
        recent_logs.append({'file': log_file, 'content': log_content})
    return recent_logs

def write_summary_of_context(context_summary: str, summary_file: str = 'summary_of_context.json') -> None:
    with open(summary_file, 'w') as file:
        json.dump(context_summary, file)

def extract_json_from_response(response: str) -> tuple[dict | None, str]:
    json_match = re.search(r'\{[\s\S]*\}', response)
    if json_match:
        try:
            json_str = json_match.group()
            # Replace escaped quotes within JSON strings
            json_str = re.sub(r'(?<!\\)\\(?!\\)"', '"', json_str)
            json_data = json.loads(json_str)
            remaining_text = response[:json_match.start()] + response[json_match.end():]
            return json_data, remaining_text.strip()
        except json.JSONDecodeError as e:
            print(f"Failed to parse JSON from response: {e}")
    return None, response

def get_directory_tree(directory: str) -> dict:
    tree = {}
    for root, dirs, files in os.walk(directory):
        rel_path = os.path.relpath(root, directory)
        if rel_path == '.':
            rel_path = ''
        node = tree
        parts = rel_path.split(os.path.sep)
        for part in parts:
            node = node.setdefault(part, {})
        for file in files:
            node[file] = None
    return tree
