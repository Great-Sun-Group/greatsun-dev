import logging
import os
import json
from datetime import datetime
from anthropic import Anthropic
from typing import Optional, Dict, Any

# Environment variables and constants
API_KEY = os.getenv("CLAUDE")
LOGS_DIRECTORY = "avatar/conversationLog"
SUMMARY_FILE = "summary_of_context.json"
AVATAR_README = "avatarREADME.md"
README = "README.md"
MESSAGE_TO_SEND = "avatar/messageToSend.txt"
CURRENT_CONTEXT_DIR = "avatar/currentContext"

os.makedirs(LOGS_DIRECTORY, exist_ok=True)
os.makedirs(CURRENT_CONTEXT_DIR, exist_ok=True)

def setup_logger() -> logging.Logger:
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    current_date = datetime.now().strftime("%Y-%m-%d")
    log_file = f"{LOGS_DIRECTORY}/{current_date}.log"
    
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(logging.INFO)
    file_formatter = logging.Formatter('%(asctime)s - %(message)s')
    file_handler.setFormatter(file_formatter)
    
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.ERROR)
    console_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(console_formatter)
    
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger

logger = setup_logger()
client = Anthropic(api_key=API_KEY)

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

def read_summary_of_context() -> list:
    try:
        with open(SUMMARY_FILE, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        logger.info("Summary of context file not found, returning empty list")
        return []
    except Exception as e:
        logger.error(f"Error reading summary of context: {e}")
        return []

def write_summary_of_context(summary: list) -> None:
    try:
        with open(SUMMARY_FILE, 'w') as file:
            json.dump(summary, file, indent=2)
        logger.info("Summary of context updated")
    except Exception as e:
        logger.error(f"Error writing summary of context: {e}")

def get_directory_tree(root_dir: str) -> Dict[str, Any]:
    directory = {}
    try:
        for item in os.listdir(root_dir):
            path = os.path.join(root_dir, item)
            if os.path.isdir(path):
                directory[item] = get_directory_tree(path)
            else:
                directory[item] = None
    except Exception as e:
        logger.error(f"Error getting directory tree: {e}")
    return directory

def main():
    while True:
        file_path = input("Optional file path (press Enter to skip, 'exit' to quit): ").strip()
        
        if file_path.lower() == "exit":
            print("Goodbye!")
            break
        
        avatar_readme_content = read_file_content(AVATAR_README)
        readme_content = read_file_content(README)
        message_to_send_content = read_file_content(MESSAGE_TO_SEND)
        included_file_content = read_file_content(file_path) if file_path else None
        
        summary_of_context = read_summary_of_context()

        directory_tree_json = json.dumps(get_directory_tree("/workspaces/greatsun-dev"))
        
        message_content = "\n\n".join(filter(None, [
            avatar_readme_content,
            readme_content,
            message_to_send_content,
            f"# Summary of context\n{json.dumps(summary_of_context, indent=2)}",
            f"# Directory structure\n{directory_tree_json}",
            f"# Attached file path \n{file_path}" if file_path else None,
            f"# Attached file contents\n{included_file_content}" if included_file_content else None
        ]))
        
        write_to_file(os.path.join(CURRENT_CONTEXT_DIR, "messageSent.txt"), message_content)
        
        try:
            message = client.messages.create(
                model="claude-3-sonnet-20240229",
                max_tokens=4096,
                messages=[
                    {"role": "user", "content": message_content}
                ]
            )
            
            avatar_response = message.content[0].text
            
            print(f"Avatar: {avatar_response}")
            logger.info(f"File: {file_path}")
            logger.info(f"Avatar: {avatar_response}")
            
            write_to_file(os.path.join(CURRENT_CONTEXT_DIR, "responseReceived.txt"), avatar_response)
            
            try:
                response_json = json.loads(avatar_response)
                
                file_contents_update = response_json.get("update_file_contents")
                file_path_update = response_json.get("update_file_path")
                if file_contents_update and file_path_update:
                    write_to_file(file_path_update, file_contents_update)
                    logger.info(f"File overwritten: {file_path_update}")
                
                updated_summary = response_json.get("summary_of_context")
                if updated_summary:
                    write_summary_of_context(updated_summary)            
            except json.JSONDecodeError:
                logger.error("Error parsing JSON response")
        except Exception as e:
            logger.error(f"Error communicating with Anthropic API: {e}")

if __name__ == "__main__":
    main()