import os
import sys
from anthropic import Anthropic
from utils.file_operations import setup_logger, read_file_content, write_to_file
from utils.ai_processing import process_ai_response, extract_json_from_response
from utils.message_handling import get_message_content

# Constants
API_KEY = os.getenv("CLAUDE")
if not API_KEY:
    raise ValueError("CLAUDE API key not found in environment variables")

LOGS_DIRECTORY = "avatar/logs"
RESPONSE_INSTRUCTIONS = "avatar/context/responseInstructions.md"
AVATAR_README = "avatar/context/avatarREADME.md"
README = "README.md"
MESSAGE_TO_SEND = "avatar/messageToSend.txt"
CONTEXT_DIR = "avatar/context"
TERMINAL_COMMANDS_FILE = "avatar/terminalCommands.txt"
CURRENT_RESPONSE_FILE = "avatar/currentResponse.txt"

# Ensure directories exist
os.makedirs(LOGS_DIRECTORY, exist_ok=True)
os.makedirs(CONTEXT_DIR, exist_ok=True)
os.makedirs(os.path.dirname(TERMINAL_COMMANDS_FILE), exist_ok=True)
os.makedirs(os.path.dirname(CURRENT_RESPONSE_FILE), exist_ok=True)

logger = setup_logger()
client = Anthropic(api_key=API_KEY)

def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')

def main():
    clear_terminal()
    print("welcome, this is the greatsun-dev environment")
    print("enter your message to me in avatar/messageToSend.txt, then press enter")
    print("before you press enter, you can optionally paste a file path as a starting point for my work")
    print("@ryanlukewatson:")

    while True:
        file_path = input().strip()
        
        if file_path.lower() == "down":
            print("greatsun-dev, over and out.")
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