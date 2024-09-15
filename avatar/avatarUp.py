import logging
import os
import json
from datetime import datetime
from anthropic import Anthropic
from typing import Optional, Dict, Any, List
import re
from utils import read_file_content, write_to_file, read_recent_logs, write_summary_of_context, get_directory_tree

# Constants
API_KEY = os.getenv("CLAUDE")
LOGS_DIRECTORY = "avatar/context/conversationLog"
SUMMARY_FILE = os.path.join("avatar", "context", "context_summary.json")
RESPONSE_INSTRUCTIONS = "avatar/context/responseInstructions.md"
AVATAR_README = "avatarREADME.md"
README = "README.md"
MESSAGE_TO_SEND = "avatar/messageToSend.md"
CONTEXT_DIR = "avatar/context"
TERMINAL_COMMANDS_FILE = "avatar/terminalCommands.txt"
CURRENT_RESPONSE_FILE = "avatar/currentResponse"

# Ensure directories exist
os.makedirs(LOGS_DIRECTORY, exist_ok=True)
os.makedirs(CONTEXT_DIR, exist_ok=True)
os.makedirs(os.path.dirname(TERMINAL_COMMANDS_FILE), exist_ok=True)
os.makedirs(os.path.dirname(CURRENT_RESPONSE_FILE), exist_ok=True)

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
client = Anthropic(api_key=API_KEY)

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

def process_ai_response(response_json: Optional[Dict[str, Any]], remaining_text: str) -> None:
    if response_json:
        # Handle file update
        file_contents_update = response_json.get("update_file_contents")
        file_path_update = response_json.get("update_file_path")
        if file_contents_update and file_path_update:
            write_to_file(file_path_update, file_contents_update)
            logger.info(f"File updated: {file_path_update}")
        
        # Handle context summary update
        context_summary = response_json.get("context_summary")
        if context_summary:
            write_summary_of_context(context_summary)
            logger.info("Context summary updated")
        
        # Handle terminal command
        terminal_command = response_json.get("terminal_command")
        if terminal_command:
            write_to_file(TERMINAL_COMMANDS_FILE, terminal_command + "\n")
            logger.info(f"Terminal command written to '{TERMINAL_COMMANDS_FILE}': {terminal_command}")
        
        # Handle response
        response_text = response_json.get("response", "")
        if remaining_text:
            response_text += f"\n\nAdditional information:\n{remaining_text}"
        
        if response_text:
            write_to_file(CURRENT_RESPONSE_FILE, response_text)
            logger.info(f"Response written to '{CURRENT_RESPONSE_FILE}'")  
    else:
        logger.warning("No valid JSON found in the response.")
        write_to_file(CURRENT_RESPONSE_FILE, remaining_text)
        logger.info(f"Full response written to '{CURRENT_RESPONSE_FILE}'")

def get_message_content(file_path: str, included_file_content: Optional[str]) -> str:
    content_parts = [
        read_file_content(RESPONSE_INSTRUCTIONS),
        read_file_content(AVATAR_README),
        read_file_content(README),
        f"# **Current Avatar Instructions from Developer**",
        read_file_content(MESSAGE_TO_SEND),
        f"## Summary of context\n\n## Attached file path \n{file_path}" if file_path else None,
        f"### Attached file contents\n{included_file_content}" if included_file_content else None,
        f"### Last 15 minutes of logs\n{json.dumps(read_recent_logs(), indent=2)}",
        f"### Directory structure\n{json.dumps(get_directory_tree('/workspaces/greatsun-dev'))}",
        read_file_content(RESPONSE_INSTRUCTIONS)
    ]
    return "\n\n".join(filter(None, content_parts))

def main():
    while True:
        file_path = input("Optional file path (press Enter to skip, 'exit' to quit): ").strip()
        
        if file_path.lower() == "exit":
            print("Goodbye!")
            break
        
        included_file_content = read_file_content(file_path) if file_path else None
        message_content = get_message_content(file_path, included_file_content)
        
        write_to_file(os.path.join(CONTEXT_DIR, "messageSent.txt"), message_content)
        
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
            
            write_to_file(os.path.join(CONTEXT_DIR, "fullResponseReceived.txt"), avatar_response)
            
            response_json, remaining_text = extract_json_from_response(avatar_response)
            process_ai_response(response_json, remaining_text)
            
        except Exception as e:
            logger.error(f"Error communicating with Anthropic API: {e}")

if __name__ == "__main__":
    main()
