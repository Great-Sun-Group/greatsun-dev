import os
import json
from typing import Optional, Dict, Any, List
from anthropic import Anthropic
from utils import setup_logger, read_file_content, write_to_file, read_recent_logs, write_summary_of_context, extract_json_from_response, get_directory_tree

# Constants
API_KEY = os.getenv("CLAUDE")
if not API_KEY:
    raise ValueError("CLAUDE API key not found in environment variables")

LOGS_DIRECTORY = "avatar/context/conversationLog"
RESPONSE_INSTRUCTIONS = "avatar/context/responseInstructions.md"
AVATAR_README = "avatarREADME.md"
README = "README.md"
MESSAGE_TO_SEND = "avatar/messageToSend.md"
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

def process_ai_response(response_json: Optional[Dict[str, Any]], remaining_text: str) -> tuple[List[str], bool]:
    requested_files = []
    actions_recommended = False

    if response_json:
        # Handle response
        response_text = response_json.get("response", "")
        if remaining_text:
            response_text += f"\n\nAdditional information:\n{remaining_text}"
        write_to_file(os.path.join(os.getcwd(), CURRENT_RESPONSE_FILE), response_text)
        logger.info(f"Response written to '{CURRENT_RESPONSE_FILE}'")

        # Handle file requests
        for i in range(1, 5):  # Assuming up to 4 file requests
            file_key = f"file_requested_{i}"
            if file_key in response_json:
                # Clean the file path
                clean_file_path = response_json[file_key].strip('"{}')
                requested_files.append(clean_file_path)
        
        if requested_files:
            logger.info(f"Files requested: {', '.join(requested_files)}")
        else:
            actions_recommended = True
            logger.info("No files requested. Processing recommended actions.")

        # Handle context summary update
        context_summary = response_json.get("context_summary")
        if context_summary:
            write_summary_of_context(context_summary)
            logger.info("Context summary updated")

        # Handle terminal command
        terminal_command = response_json.get("terminal_command")
        if terminal_command:
            with open(os.path.join(os.getcwd(), TERMINAL_COMMANDS_FILE), "a") as file:
                file.write(terminal_command + "\n")
            logger.info(f"Terminal command written to '{TERMINAL_COMMANDS_FILE}': {terminal_command}")

        # Handle file updates
        for i in range(1, 6):
            update_file_path = response_json.get(f"update_file_path_{i}")
            update_file_contents = response_json.get(f"update_file_contents_{i}")
            if update_file_path and update_file_contents:
                abs_file_path = os.path.join(os.getcwd(), update_file_path)
                write_to_file(abs_file_path, update_file_contents)
                logger.info(f"File updated: {abs_file_path}")
                actions_recommended = True
    else:
        logger.warning("No valid JSON found in the response.")
        write_to_file(os.path.join(os.getcwd(), CURRENT_RESPONSE_FILE), remaining_text)
        logger.info(f"Full response written to '{CURRENT_RESPONSE_FILE}'")

    return requested_files, actions_recommended

def get_message_content(file_path: str, included_content: Optional[str], requested_files: List[str] = None) -> str:
    content_parts = [
        read_file_content(RESPONSE_INSTRUCTIONS),
        read_file_content(AVATAR_README),
        read_file_content(README),
        "# **Current Avatar Instructions from Developer**",
        read_file_content(MESSAGE_TO_SEND),
        f"""## Summary of context

## Attached path 
{file_path}""" if file_path else None,
        f"""### Attached path contents
{included_content}""" if included_content else None,
    ]

    if requested_files:
        for file in requested_files:
            # Remove any extra quotation marks and curly braces
            clean_file_path = file.strip('"{}')
            # Use os.path.join to create a proper file path
            full_path = os.path.join('/workspaces/greatsun-dev', clean_file_path)
            content = read_file_content(full_path)
            if content:
                content_parts.append(f"### Contents of {clean_file_path}\n{content}")
            else:
                content_parts.append(f"### File {clean_file_path} not found or empty")

    content_parts.extend([
        f"""### Last 15 minutes of logs
{read_recent_logs(minutes=15)}""",
        f"""### Directory structure
{json.dumps(get_directory_tree('/workspaces/greatsun-dev'), indent=2)}""",
        read_file_content(RESPONSE_INSTRUCTIONS)
    ])

    return "\n\n".join(filter(None, content_parts))

def main():
    while True:
        file_path = input("Optional file path (press Enter to skip, 'exit' to quit): ").strip()
        
        if file_path.lower() == "exit":
            print("Goodbye!")
            break
        
        included_content = read_file_content(file_path) if file_path else None
        requested_files = []
        provided_files = set()
        
        while True:
            message_content = get_message_content(file_path, included_content, requested_files)
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
                new_requested_files, actions_recommended = process_ai_response(response_json, remaining_text)
                
                if actions_recommended:
                    print("AI has recommended actions. These have been processed and written to the appropriate files.")
                    logger.info("AI recommended actions processed.")
                    break  # Break the inner loop to get a new file path from the user
                
                if new_requested_files:
                    # Filter out files that have already been provided
                    new_requested_files = [f for f in new_requested_files if f not in provided_files]
                    if new_requested_files:
                        print(f"AI has requested additional files: {', '.join(new_requested_files)}")
                        logger.info(f"AI requested additional files: {', '.join(new_requested_files)}")
                        requested_files = new_requested_files
                        provided_files.update(new_requested_files)
                    else:
                        print("AI requested files that have already been provided. Moving to next iteration.")
                        break  # Break the inner loop to get a new file path from the user
                else:
                    print("AI didn't request any new files or recommend actions. Please provide a new file path.")
                    logger.info("AI didn't request new files or recommend actions.")
                    break  # Break the inner loop to get a new file path from the user
                
            except Exception as e:
                logger.error(f"Error communicating with Anthropic API: {e}")
                print(f"An error occurred: {e}")
                break  # Break the inner loop on error

if __name__ == "__main__":
    main()