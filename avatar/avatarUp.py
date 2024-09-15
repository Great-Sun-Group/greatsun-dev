import os
from anthropic import Anthropic
from utils.constants import API_KEY, CONTEXT_DIR
from utils.file_operations import setup_logger, write_to_file, read_file_content
from utils.ai_processing import process_ai_response, extract_json_from_response
from utils.message_handling import get_message_content

logger = setup_logger()
client = Anthropic(api_key=API_KEY)

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
                    break

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
                        break
                else:
                    print("AI didn't request any new files or recommend actions. Please provide a new file path.")
                    logger.info("AI didn't request new files or recommend actions.")
                    break

            except Exception as e:
                            logger.error(f"Error communicating with Anthropic API: {e}")
                            print(f"An error occurred: {e}")
                            break

            if file_request_count >= max_file_requests:
                print(f"Reached the maximum number of file requests ({max_file_requests}). Starting a new conversation.")
                file_request_count = 0
                provided_files.clear()

    if __name__ == "__main__":
        main()