import os
import json
import logging
from typing import Optional, List
from anthropic import Anthropic

# Configure logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Constants
ANTHROPIC_API_KEY = os.getenv('ANTHROPIC_API_KEY')
# GitHub username of the current developer
GREATSUN_DEVELOPER = os.getenv('GITHUB_USERNAME')
FINAL_MESSAGE_MARKER = "** @avatarParserSection: FINAL RESPONSE TO DEVELOPER **"
UPDATE_FILE_PATH_MARKER = "** @avatarParserSection: FILE PATH TO WRITE **"
UPDATE_FILE_CONTENT_MARKER = "** @avatarParserSection: FILE CONTENT TO WRITE **"
REQUESTED_FILES_MARKER = "** @avatarParserSection: LIST OF UP TO SEVEN FILES REQUESTED FOR CONTEXT BY THE LLM**"
PARSER_SECTION_END_MARKER = "** @avatarParserSection: SECTION END **"

# Initialize Anthropic client
large_language_model = Anthropic(api_key=ANTHROPIC_API_KEY)


def read_file(file_path: str) -> str:
    """
    Read and return contents of a file with error handling.
    If the path is a directory, log it and return a message.

    Args:
        file_path (str): Path to the file or directory

    Returns:
        str: File contents or a message if it's a directory
    """
    try:
        if os.path.isdir(file_path):
            logger.info(f"{file_path} is a directory")
            return "The reference is to a directory."
        with open(file_path, 'r') as file:
            return file.read()
    except FileNotFoundError:
        logger.error(f"File not found: {file_path}")
        return f"Error: File {file_path} not found"
    except IOError as e:
        logger.error(f"IO error occurred while reading {file_path}: {e}")
        return f"Error: Unable to read {file_path}"


def write_file(file_path: str, file_content: str) -> None:
    """
    Write content to a file, creating it if it doesn't exist.

    Args:
        file_path (str): Path to the file
        file_content (str): Content to write to the file
    """
    try:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'w') as file:
            file.write(file_content)
        logger.info(f"Successfully wrote to {file_path}")
    except IOError as e:
        logger.error(f"Error writing to {file_path}: {e}")


def get_directory_tree(path: str) -> dict:
    """
    Generate a directory tree structure.

    Args:
        path (str): Root path to start the tree

    Returns:
        dict: Directory tree structure
    """
    tree = {}
    for entry in os.scandir(path):
        if entry.is_dir():
            tree[entry.name] = get_directory_tree(entry.path)
        else:
            tree[entry.name] = None
    return tree


def extract_section(text: str, start_marker: str, end_marker: str) -> str:
    """
    Extract a section of text between two markers.

    Args:
        text (str): Full text to search
        start_marker (str): Start marker of the section
        end_marker (str): End marker of the section

    Returns:
        str: Extracted text between markers
    """
    start = text.find(start_marker)
    if start == -1:
        return ""
    start += len(start_marker)
    end = text.find(end_marker, start)
    if end == -1:


        return text[start:].strip()
    return text[start:end].strip()

def process_llm_response(response: str) -> tuple:
    """
    Process the LLM response and extract relevant sections.

    Args:
        response (str): LLM response text

    Returns:
        tuple: Contains extracted sections (avatar_response, update_file_path, update_file_content, files_requested)
    """
    avatar_response = extract_section(response, FINAL_MESSAGE_MARKER, PARSER_SECTION_END_MARKER)
    update_file_path = extract_section(response, UPDATE_FILE_PATH_MARKER, PARSER_SECTION_END_MARKER)
    update_file_content = extract_section(response, UPDATE_FILE_CONTENT_MARKER, PARSER_SECTION_END_MARKER)
    files_requested = extract_section(response, REQUESTED_FILES_MARKER, PARSER_SECTION_END_MARKER).split('\n')
    return avatar_response, update_file_path, update_file_content, files_requested

def main():
    """
    Main function to run the avatar environment.
    """
    os.system('cls' if os.name == 'nt' else 'clear')
    print("Welcome to the greatsun-dev avatar environment")
    print("Enter your instructions or questions in avatar/messageFromDeveloper.md")
    print("Then press enter here in the terminal, and you can first")
    print("optionally paste a file path, as a starting point for my work.")
    print(f"{GREATSUN_DEVELOPER}: ", end="", flush=True)

    while True:
        file_path = input().strip()

        if file_path.lower() == "down":
            print("\ngreatsun-dev avatar, signing off\n\n")
            break

        message_from_developer = read_file("avatar/messageFromDeveloper.md")
        reference_file_content = read_file(file_path) if file_path else None
        trigger_message_content = f"{message_from_developer}\n{file_path}\n{reference_file_content}"

        avatar_up = "\n".join([
            read_file("avatar/avatarOrientation.md"),
            read_file("avatar/avatarUp.py"),
            "** This is the project README.md **",
            read_file("README.md"),
            "** IMPORTANT IMPORTANT IMPORTANT: Current Instructions from Developer **",
            trigger_message_content,
            "Full Project Structure:",
            json.dumps(get_directory_tree('/workspaces/greatsun-dev'), indent=2),
            "** END avatarUp message **"
        ])
        write_file("avatar/avatarConversation.txt", avatar_up)

        # START LLM LOOP, allow to run up to 7 iterations
        for _ in range(7):
            try:
                llm_message = read_file("avatar/avatarConversation.txt")
                llm_call = large_language_model.messages.create(
                    model="claude-3-5-sonnet-20240620",
                    max_tokens=4096,
                    messages=[
                        {"role": "user", "content": llm_message}
                    ]
                )
                llm_response = llm_call.content[0].text
                write_file("avatar/avatarConversation.txt", f"{llm_message}\n{llm_response}")

                avatar_response, update_file_path, update_file_content, files_requested = process_llm_response(llm_response)

                if avatar_response:
                    write_file("avatar/avatarResponseToDeveloper.md", avatar_response)
                    print("Avatar:")
                    print(avatar_response)
                    break  # End LLM loop


                if update_file_path and update_file_content:
                    write_file(update_file_path, update_file_content)
                    print(f"File updated: {update_file_path}")

                    if files_requested:
                        files_requested_contents = ""
                    for file_requested in files_requested:
                        if file_requested.strip():
                            file_content = read_file(file_requested.strip())
                            files_requested_contents += f"{file_requested}\n{file_content}\n\n"
                            print(f"File requested: {file_requested}")
                    write_file("avatar/avatarConversation.txt",
                               f"{llm_message}\n{llm_response}\n{files_requested_contents}")

            except Exception as e:
                logger.error(f"Error in LLM loop: {e}")
                final_response = "Sorry, an error occurred while processing the LLM response. Let's try again, or try another model."
                write_file("avatar/avatarResponseToDeveloper.md", final_response)
                print(final_response)
                break  # End LLM loop on error

        else:  # This else clause is executed if the for loop completes without breaking
            final_response = "Sorry, the LLM we queried was unable to successfully engage with me after 7 iterations. Let's try again, or try another model."
            write_file("avatar/avatarResponseToDeveloper.md", final_response)
            avatar_conversation = read_file("avatar/avatarConversation.txt")
            write_file("avatar/avatarConversation.txt", f"{avatar_conversation}\n{final_response}")
            print(final_response)

if __name__ == "__main__":
    main()