import os
import sys
from anthropic import Anthropic
from utils.file_operations import setup_logger, read_file_content, write_to_file
from utils.ai_processing import process_ai_response, extract_json_from_response
from utils.message_handling import get_message_content
from utils.constants import LOGS_DIRECTORY, ANTHROPIC_API_KEY, CONTEXT_DIR, CURRENT_RESPONSE_FILE

# Ensure directories exist
os.makedirs(LOGS_DIRECTORY, exist_ok=True)
os.makedirs(CONTEXT_DIR, exist_ok=True)
os.makedirs(os.path.dirname(CURRENT_RESPONSE_FILE), exist_ok=True)

logger = setup_logger()
client = Anthropic(api_key=ANTHROPIC_API_KEY)

def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')


def main():
    clear_terminal()
    print("welcome to this dev environment")
    print("I'm the greatsun-dev avatar")
    print("enter your message to me in avatar/messageToSend.txt, then press enter")
    print("before you press enter, you can optionally paste a file path as a starting point for my work")
    print("@ryanlukewatson:")

    while True:
        file_path = input().strip()

        if file_path.lower() == "down":
            print("\ngreatsun-dev, over and out.")
            break

        included_file_content = read_file_content(
            file_path) if file_path else None
        message_content = get_message_content(file_path, included_file_content)

        write_to_file(os.path.join(
            CONTEXT_DIR, "messageSent.txt"), message_content)

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

            write_to_file(os.path.join(
                CONTEXT_DIR, "fullResponseReceived.txt"), avatar_response)

            response_json, remaining_text = extract_json_from_response(
                avatar_response)
            requested_files, actions_recommended, additional_files_to_update = process_ai_response(
                response_json, remaining_text)

            # Handle requested files
            if requested_files:
                file_contents = []
                for req_file in requested_files:
                    content = read_file_content(req_file)
                    if content:
                        file_contents.append(
                            f"File: {req_file}\n\nContent:\n{content}")
                    else:
                        file_contents.append(
                            f"File: {req_file}\n\nUnable to read file content.")

                if file_contents:
                    additional_message = "Here are the contents of the requested files:\n\n" + \
                        "\n\n".join(file_contents)
                    write_to_file(os.path.join(
                        CONTEXT_DIR, "messageSent.txt"), additional_message)

                    # Send another message to the AI with the file contents
                    follow_up_message = client.messages.create(
                        model="claude-3-sonnet-20240229",
                        max_tokens=4096,
                        messages=[
                            {"role": "user", "content": additional_message}
                        ]
                    )

                    follow_up_response = follow_up_message.content[0].text
                    print(f"Avatar: {follow_up_response}")
                    logger.info(f"Avatar (follow-up): {follow_up_response}")
                    write_to_file(os.path.join(
                        CONTEXT_DIR, "fullResponseReceived.txt"), follow_up_response)

                    # Process the follow-up response
                    follow_up_json, follow_up_remaining_text = extract_json_from_response(
                        follow_up_response)
                    process_ai_response(
                        follow_up_json, follow_up_remaining_text)

            print("\n@ryanlukewatson:")

        except Exception as e:
            logger.error(f"Error communicating with Anthropic API: {e}")
            print(f"An error occurred: {e}")
            print("\n@ryanlukewatson:")


if __name__ == "__main__":
    main()
