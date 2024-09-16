import json
import os
import logging
from anthropic import Anthropic
from avatarUpCommands import cross_repo_commit

# Configure logging
logging.basicConfig(filename='avatar.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Constants
ANTHROPIC_API_KEY = os.environ.get('CLAUDE')
GITHUB_USERNAME = os.environ.get('GITHUB_USERNAME')
MAX_LLM_ITERATIONS = 7

# Markers for parsing LLM responses
FINAL_MESSAGE_MARKER = "**@avatarParserSection: FINAL_RESPONSE_TO_DEVELOPER **"
UPDATE_FILE_MARKER = "**@avatarParserSection: FILE_TO_WRITE: "
REQUESTED_FILES_MARKER = "**@avatarParserSection: LIST_OF_FILES_REQUESTED_FOR_CONTEXT_BY_THE_LLM **"
PARSER_SECTION_END_MARKER = "**@avatarParserSection: SECTION_END **"

# Initialize Anthropic client
large_language_model = Anthropic(api_key=ANTHROPIC_API_KEY)
greatsun_developer = GITHUB_USERNAME


def read_file(file_path):
    """
    Robust function to read and return contents of a file, with solid error handling.
    If passed the path to a directory, it checks that it is a directory, logs that, and returns a message.

    Args:
    file_path (str): Path to the file or directory to be read

    Returns:
    str: Contents of the file or a message indicating it's a directory
    """
    try:
        if os.path.isdir(file_path):
            logging.info(f"Attempted to read directory: {file_path}")
            return "The reference is to a directory."

        with open(file_path, 'r') as file:
            content = file.read()
        logging.info(f"Successfully read file: {file_path}")
        return content
    except FileNotFoundError:
        logging.error(f"File not found: {file_path}")
        return f"Error: File not found - {file_path}"
    except PermissionError:
        logging.error(
            f"Permission denied when trying to read file: {file_path}")
        return f"Error: Permission denied - {file_path}"
    except Exception as e:
        logging.error(
            f"Unexpected error when reading file {file_path}: {str(e)}")
        return f"Error: Unexpected issue when reading file - {file_path}"


def write_file(file_path, file_content):
    """
    Robust function that will create the file if it doesn't exist and write over what is there if it does exist,
    with solid error handling.

    Args:
    file_path (str): Path to the file to be written
    file_content (str): Content to be written to the file

    Returns:
    bool: True if write operation was successful, False otherwise
    """
    try:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'w') as file:
            file.write(file_content)
        logging.info(f"Successfully wrote to file: {file_path}")
        return True
    except PermissionError:
        logging.error(
            f"Permission denied when trying to write to file: {file_path}")
        return False
    except Exception as e:
        logging.error(
            f"Unexpected error when writing to file {file_path}: {str(e)}")
        return False


def extract_content(text, start_marker, end_marker):
    """
    Extract content between two markers in a text.

    Args:
    text (str): The text to search in
    start_marker (str): The starting marker
    end_marker (str): The ending marker

    Returns:
    str: The extracted content, or None if not found
    """
    start = text.find(start_marker)
    if start == -1:
        return None
    start += len(start_marker)
    end = text.find(end_marker, start)
    if end == -1:
        return None
    return text[start:end].strip()


def get_directory_tree(path):
    """
    Generate a directory tree structure.

    Args:
    path (str): The root path to start from

    Returns:
    dict: A nested dictionary representing the directory structure
    """
    tree = {}
    for entry in os.scandir(path):
        if entry.is_dir():
            tree[entry.name] = get_directory_tree(entry.path)
        else:
            tree[entry.name] = None
    return tree


def process_llm_response(llm_response):
    """
    Process the LLM response, extracting relevant information and updating files as necessary.

    Args:
    llm_response (str): The response from the LLM

    Returns:
    tuple: (bool, str) - (whether to continue the LLM loop, extracted response to developer)
    """
    # Extract response to developer
    avatar_response = extract_content(
        llm_response, FINAL_MESSAGE_MARKER, PARSER_SECTION_END_MARKER)
    if avatar_response:
        write_file("avatar/avatarResponseToDeveloper.md", avatar_response)
        print("Avatar:")
        print(avatar_response)
        return False, avatar_response

    # Process file updates
    update_marker_index = llm_response.find(UPDATE_FILE_MARKER)
    while update_marker_index != -1:
        end_bracket = llm_response.find(']', update_marker_index)
        file_path = llm_response[update_marker_index +
                                 len(UPDATE_FILE_MARKER):end_bracket]
        file_content = extract_content(
            llm_response[end_bracket:], "**", PARSER_SECTION_END_MARKER)
        if file_content:
            if write_file(file_path, file_content):
                print(f"File updated: {file_path}")
            else:
                print(f"Failed to update file: {file_path}")
        update_marker_index = llm_response.find(
            UPDATE_FILE_MARKER, end_bracket)

    # Process requested files
    requested_files = extract_content(
        llm_response, REQUESTED_FILES_MARKER, PARSER_SECTION_END_MARKER)
    if requested_files:
        files_requested_contents = ""
        for file_path in requested_files.split('\n'):
            file_path = file_path.strip()
            if file_path:
                file_content = read_file(file_path)
                files_requested_contents += f"File: {file_path}\n\n{file_content}\n\n"
                print(f"File requested: {file_path}")

        current_conversation = read_file("avatar/avatarConversation.txt")
        write_file("avatar/avatarConversation.txt",
                   current_conversation + files_requested_contents)

    return True, None


def main():
    first_run = True
    """
    Main function to run the avatar environment.
    """
    os.system('cls' if os.name == 'nt' else 'clear')
    print("Welcome to the greatsun-dev avatar environment")
    print("Enter your instructions or questions in avatar/messageFromDeveloper.md")
    print("Then press enter here in the terminal, or you can first")
    print("Optionally paste a file path as a starting point for my work")
    print(f"{greatsun_developer}: ")

    while True:
        file_path = input().strip()

        if file_path.lower() == "avatar down":
            print("\ngreatsun-dev avatar, signing off\n\n")
            break

        if file_path.lower() == "avatar commit":
            commit_id = cross_repo_commit()
            if commit_id:
                write_file("avatar/avatarConversation.txt",
                           "ready for conversation")
                print(f"Commit {commit_id} made and avatar cleared")
                continue


            if file_path.lower() == "avatar clear":
                write_file("avatar/avatarConversation.txt", "ready for conversation")
                print("Avatar cleared")
                first_run = True  # Reset the flag when clearing
                continue
            
        # Prepare the message from the developer
        message_from_developer = read_file("avatar/messageFromDeveloper.md")
        reference_file_content = read_file(
            file_path) if file_path else "No reference file provided."
        trigger_message_content = f"{message_from_developer}\n\nReference File: {file_path}\n\n{reference_file_content}"

        if first_run:
            # Prepare the full context for the LLM (first run)
            avatar_up_content = [
                read_file("avatar/avatarOrientation.md"),
                read_file("avatar/avatarUp.py"),
                "** This is the project README.md **",
                read_file("README.md"),
                "** This is the credex-core submodule README.md **",
                read_file("credex-ecosystem/credex-core/README.md"),
                "** This is the vimbiso-pay submodule README.md **",
                read_file("credex-ecosystem/vimbiso-pay/README.md"),
                "** IMPORTANT IMPORTANT IMPORTANT: Current Instructions from Developer: the purpose of this conversation **",
                trigger_message_content,
                "Full Project Structure:",
                json.dumps(get_directory_tree(
                    '/workspaces/greatsun-dev'), indent=2),
                "** END avatarUp message **\n"
            ]
            avatar_up = "\n\n".join(avatar_up_content)
            write_file("avatar/avatarConversation.txt", avatar_up)
            first_run = False
        else:
            # For subsequent runs, append to existing conversation
            existing_conversation = read_file("avatar/avatarConversation.txt")
            updated_conversation = f"{existing_conversation}\n\n** New input from developer **\n\n{trigger_message_content}\n"
            write_file("avatar/avatarConversation.txt", updated_conversation)

        # START LLM LOOP, allow to run up to MAX_LLM_ITERATIONS iterations
        for iteration in range(MAX_LLM_ITERATIONS):
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
                write_file("avatar/avatarConversation.txt",
                           llm_message + llm_response)

                continue_loop, avatar_response = process_llm_response(
                    llm_response)

                if not continue_loop:
                    break  # Exit the LLM loop if we have a final response


            except Exception as e:
                logging.error(f"Error in LLM loop: {str(e)}")
                avatar_response = f"Sorry, an error occurred while processing your request: {str(e)}"
                write_file("avatar/avatarResponseToDeveloper.md",
                           avatar_response)
                break  # Exit the LLM loop on error

        else:
            # This block executes if the for loop completes without breaking
            final_response = "Sorry, the LLM we queried was unable to successfully complete the task within the maximum allowed iterations. Let's try again, or consider using another model."
            write_file("avatar/avatarResponseToDeveloper.md", final_response)
            avatar_conversation = read_file("avatar/avatarConversation.txt")
            write_file("avatar/avatarConversation.txt", avatar_conversation + "\n\n" + final_response)
            print(final_response)

        # Print the final response to the developer
        print("\nAvatar Response:")
        print(read_file("avatar/avatarResponseToDeveloper.md"))
        print("\nReady for next input. Type 'avatar down' to exit.")

if __name__ == "__main__":
    main()