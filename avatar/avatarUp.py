import os
from anthropic import Anthropic
from utils import setup_logger, read_file_content, write_to_file, read_recent_logs, write_summary_of_context, extract_json_from_response, get_directory_tree

# Constants
API_KEY = os.getenv("CLAUDE")
LOGS_DIRECTORY = "avatar/context/conversationLogs"
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

logger = setup_logger(LOGS_DIRECTORY)
client = Anthropic(api_key=API_KEY)

def process_ai_response(response_json: dict | None, remaining_text: str) -> None:
    if response_json:
        for key, value in response_json.items():
            if value:
                logger.info(f"Processing {key}")
                if key.startswith("update_file_path"):
                    index = key.split("_")[-1]
                    content_key = f"update_file_contents_{index}"
                    if content_key in response_json:
                        write_to_file(value, response_json[content_key])
                        logger.info(f"Updated file: {value}")
                    else:
                        logger.warning(f"Missing content for file: {value}")
                elif key == "terminal_command":
                    with open(TERMINAL_COMMANDS_FILE, "a") as f:
                        f.write(value + "\\n")
                    logger.info(f"Added terminal command: {value}")
                elif key == "context_summary":
                    write_summary_of_context(value)
                    logger.info("Updated context summary")
                elif key == "response":
                    write_to_file(CURRENT_RESPONSE_FILE, value)
                    logger.info(f"Wrote response to {CURRENT_RESPONSE_FILE}")
    else:
        logger.warning("No valid JSON found in the response.")
    
    if remaining_text:
        write_to_file(os.path.join(CONTEXT_DIR, "remaining_text.txt"), remaining_text)
        logger.info("Wrote remaining text to file")

def get_message_content(file_path: str, included_file_content: str | None) -> str:
    content_parts = [
        read_file_content(RESPONSE_INSTRUCTIONS),
        read_file_content(AVATAR_README),
        read_file_content(README),
        f"# **Current Avatar Instructions from Developer**",
        read_file_content(MESSAGE_TO_SEND),
        f"## Summary of context\\n\\n## Attached file path \\n{file_path}" if file_path else None,
        f"### Attached file contents\\n{included_file_content}" if included_file_content else None,
        f"### Last 15 minutes of logs\\n{json.dumps(read_recent_logs(LOGS_DIRECTORY), indent=2)}",
        f"### Directory structure\\n{json.dumps(get_directory_tree('/workspaces/greatsun-dev'))}",
        read_file_content(RESPONSE_INSTRUCTIONS)
    ]
    return "\\n\\n".join(filter(None, content_parts))

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