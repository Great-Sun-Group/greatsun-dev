import logging
import os
import json
from datetime import datetime
from anthropic import Anthropic

api_key = os.getenv("CLAUDE")

logs_directory = "conversationLog"
os.makedirs(logs_directory, exist_ok=True)

def setup_logger():
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    current_date = datetime.now().strftime("%Y-%m-%d")
    log_file = f"{logs_directory}/{current_date}.log"
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(message)s')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    return logger

logger = setup_logger()
client = Anthropic(api_key=api_key)

def read_file_content(file_path):
    try:
        with open(file_path, 'r') as file:
            return file.read()
    except FileNotFoundError:
        logger.error(f"File not found: {file_path}")
        return None
    except Exception as e:
        logger.error(f"Error reading file: {e}")
        return None

def write_to_file(file_path, content):
    try:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'w') as file:
            file.write(content)
        logger.info(f"Content written to {file_path}")
    except Exception as e:
        logger.error(f"Error writing to file: {file_path}, {e}")

def read_summary_of_context():
    file_path = "summary_of_context.json"
    try:
        with open(file_path, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        logger.info("Summary of context file not found, returning empty list")
        return []
    except Exception as e:
        logger.error(f"Error reading summary of context: {e}")
        return []

def write_summary_of_context(summary):
    file_path = "summary_of_context.json"
    try:
        with open(file_path, 'w') as file:
            json.dump(summary, file, indent=2)
        logger.info("Summary of context updated")
    except Exception as e:
        logger.error(f"Error writing summary of context: {e}")

while True:
    file_path = input("Optional file path (press Enter to skip): ").strip()
    
    if file_path.lower() == "exit":
        print("Goodbye!")
        break
    
    avatar_readme_content = read_file_content("avatarREADME.md")
    readme_content = read_file_content("README.md")
    message_to_send_content = read_file_content("avatar/messageToSend.txt")
    included_file_content = read_file_content(file_path) if file_path else None
    
    summary_of_context = read_summary_of_context()
    
    message_content = "\n\n".join(filter(None, [
        avatar_readme_content,
        readme_content,
        message_to_send_content,
        f"# Summary of context\n{json.dumps(summary_of_context, indent=2)}",
        f"# Attached file path \n{file_path}" if file_path else None,
        f"# Attached file contents\n{included_file_content}" if included_file_content else None
    ]))
    
    write_to_file("messageSent.txt", message_content)
    
    try:
        message = client.messages.create(
            model="claude-3-opus-20240229",
            max_tokens=2000,
            messages=[
                {"role": "user", "content": message_content}
            ]
        )
        
        avatar_response = message.json()['completion']
        
        print(f"Avatar: {avatar_response}")
        logger.info(f"File: {file_path}")
        logger.info(f"Avatar: {avatar_response}")
        
        write_to_file("responseReceived.txt", avatar_response)
        
        try:
            response_json = json.loads(avatar_response)
            
            file_contents_update = response_json.get("update_file_contents")
            file_path_update = response_json.get("update_file_path")
            if file_contents_update and file_path_update:
                write_to_file(file_path_update, file_contents_update)
            
            updated_summary = response_json.get("summary_of_context")
            if updated_summary:
                write_summary_of_context(updated_summary)            
        except json.JSONDecodeError:
            logger.error("Error parsing JSON response")
    except Exception as e:
        logger.error(f"Error communicating with Anthropic API: {e}")