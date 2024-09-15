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

def process_ai_response(response_json: Optional[Dict[str, Any]], remaining_text: str) -> tuple[List[str], bool, List[str]]:
    requested_files = []
    actions_recommended = False
    additional_files_to_update = []

    if response_json:
        logger.info(f"Processing AI response: {json.dumps(response_json, indent=2)}")

        # Handle response
        response_text = response_json.get("response", "")
        if remaining_text:
            response_text += f"\n\nAdditional information:\n{remaining_text}"
        write_to_file(os.path.join(os.getcwd(), CURRENT_RESPONSE_FILE), response_text)

        # Handle file requests
        for i in range(1, 8):
            file_key = f"file_requested_{i}"
            if file_key in response_json:
                requested_files.append(response_json[file_key].strip('"{}'))

        if requested_files:
            logger.info(f"Files requested: {', '.join(requested_files)}")
        else:
            actions_recommended = True

        # Handle terminal command
        terminal_command = response_json.get("terminal_command")
        if terminal_command:
            with open(os.path.join(os.getcwd(), TERMINAL_COMMANDS_FILE), "a") as file:
                file.write(terminal_command + "\n")

        # Handle file update
        update_file_path = response_json.get("update_file_path")
        update_file_contents = response_json.get("update_file_contents")
        if update_file_path and update_file_contents:
            abs_file_path = os.path.join(os.getcwd(), update_file_path.strip('"{}'))
            write_to_file(abs_file_path, update_file_contents)
            actions_recommended = True

# Handle additional files to update
        additional_files = response_json.get("additional_files_to_update")
        if additional_files:
            additional_files_to_update = json.loads(additional_files) if isinstance(additional_files, str) else additional_files
            logger.info(f"Additional files to update: {', '.join(additional_files_to_update)}")
            actions_recommended = True
    else:
        logger.warning("No valid JSON found in the response.")
        write_to_file(os.path.join(os.getcwd(), CURRENT_RESPONSE_FILE), remaining_text)

    return requested_files, actions_recommended, additional_files_to_update

def get_message_content(file_path: str, included_content: Optional[str], requested_files: List[str] = None) -> str:
    content_parts = [
        read_file_content(RESPONSE_INSTRUCTIONS),
        read_file_content(AVATAR_README),
        read_file_content(README),
        "# **Current Avatar Instructions from Developer**",
        read_file_content(MESSAGE_TO_SEND),
        f"## Summary of context\n\n## Attached path\n{file_path}" if file_path else None,
        f"### Attached path contents\n{included_content}" if included_content else None,
    ]

    if requested_files:
        for file in requested_files:
            full_path = os.path.join('/workspaces/greatsun-dev', file.strip('"{}'))
            content = read_file_content(full_path)
            content_parts.append(f"### Contents of {file}\n{content}" if content else f"### File {file} not found or empty")

    content_parts.extend([
        f"### Last 15 minutes of logs\n{read_recent_logs(minutes=15)}",
        f"### Directory structure\n{json.dumps(get_directory_tree('/workspaces/greatsun-dev'), indent=2)}",
        read_file_content(RESPONSE_INSTRUCTIONS)
    ])

    return "\n\n".join(filter(None, content_parts))

def main():
    file_request_count = 0
    max_file_requests = 7
    provided_files = set()
    additional_files_to_update = []

    while True:
        if not additional_files_to_update:
            file_path = input("Optional file path (press Enter to skip, 'exit' to quit): ").strip()
            if file_path.lower() == "exit":
                print("Goodbye!")
                break
        else:
            file_path = additional_files_to_update.pop(0)

        included_content = read_file_content(file_path) if file_path else None
        requested_files = []

        while file_request_count < max_file_requests:
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
                new_requested_files, actions_recommended, new_additional_files = process_ai_response(response_json, remaining_text)

                if actions_recommended:
                    print("AI has recommended actions. These have been processed and written to the appropriate files.")
                    logger.info("AI recommended actions processed.")
                    if new_additional_files:
                        additional_files_to_update.extend(new_additional_files)
                        print(f"Additional files to update: {', '.join(additional_files_to_update)}")
                    break  # Break the inner loop to process the next file or get a new file path from the user

                if new_requested_files:
                    new_requested_files = [f for f in new_requested_files if f not in provided_files]
                    if new_requested_files:
                        print(f"AI has requested additional files: {', '.join(new_requested_files)}")
                        logger.info(f"AI requested additional files: {', '.join(new_requested_files)}")
                        requested_files = new_requested_files
                        provided_files.update(new_requested_files)
                        file_request_count += 1
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

        if file_request_count >= max_file_requests:
            print(f"Reached the maximum number of file requests ({max_file_requests}). Starting a new conversation.")
            file_request_count = 0
            provided_files.clear()

if __name__ == "__main__":
    main()