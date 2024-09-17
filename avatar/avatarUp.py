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
MAX_LLM_ITERATIONS = 42

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
            return f"The provided path is a directory: {file_path}"

        with open(file_path, 'r') as file:
            content = file.read()
        logging.info(f"Successfully read file: {file_path}")
        return content
    except FileNotFoundError:
        logging.error(f"File not found: {file_path}")
        return f"File not found: {file_path}"
    except Exception as e:
        logging.error(f"Error reading file {file_path}: {str(e)}")
        return f"Error reading file: {str(e)}"


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
    except Exception as e:
        logging.error(f"Error writing to file {file_path}: {str(e)}")
        return False


def get_directory_tree(path):
    """
    Recursively get the directory structure as a dictionary.

    Args:
    path (str): Path to the directory

    Returns:
    dict: Directory structure
    """
    tree = {}
    try:
        for entry in os.scandir(path):
            if entry.is_dir():
                tree[entry.name] = get_directory_tree(entry.path)
            else:
                tree[entry.name] = None
    except Exception as e:
        logging.error(f"Error getting directory tree for {path}: {str(e)}")
    return tree


def main():
    """
    Main function to run the avatar environment.
    """
    first_run = True
    os.system('cls' if os.name == 'nt' else 'clear')
    print("Welcome to the greatsun-dev avatar environment")
    print("Enter your instructions or questions in avatar/messageFromDeveloper.md")
    print("Then press enter here in the terminal, or you can first")
    print("optionally paste a file path as a starting point for my work")
    print(f"{greatsun_developer}: ")


    while True:
        file_path = input().strip()

        if file_path.lower() == "avatar down":
            print("\ngreatsun-dev avatar, signing off\n\n")
            logging.info("Avatar session ended")
            break

        if file_path.lower() == "avatar commit":
            commit_id = cross_repo_commit()
            if commit_id:
                write_file("avatar/avatarConversation.txt",
                           "ready for conversation")
                print(f"Commit {commit_id} made and avatar cleared")
                logging.info(f"Commit made with ID: {commit_id}")
                continue

        if file_path.lower() == "avatar clear":
            write_file("avatar/avatarConversation.txt",
                       "ready for conversation")
            print("Avatar cleared")
            logging.info("Avatar conversation cleared")
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
                "** This is the currentProject.md **",
                read_file("avatar/currentProject.md"),
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
            logging.info("First run context prepared and written")

        else:
            # For subsequent runs, append to existing conversation
            existing_conversation = read_file("avatar/avatarConversation.txt")
            updated_conversation = f"{existing_conversation}\n\n** New input from developer **\n\n{trigger_message_content}\n"
            write_file("avatar/avatarConversation.txt", updated_conversation)
            logging.info("Appended new developer input to conversation")

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
                conversationPlusResponse = f"{llm_message}\n\n{llm_response}"
                write_file("avatar/avatarConversation.txt",
                           conversationPlusResponse)
                logging.info(
                    f"LLM response received and written (iteration {iteration + 1})")

                # Process a requested file
                if llm_response.startswith("READ_A_FILE"):
                    lines = llm_response.split('\n', 2)
                    if len(lines) >= 2:
                        file_path_to_read = lines[1].strip()
                        read_data = f"{file_path_to_read}\n{read_file(file_path_to_read)}"
                        updated_conversation = f"{conversationPlusResponse}\n\n{read_data}"
                        write_file("avatar/avatarConversation.txt", updated_conversation)
                        print(f"READ_A_FILE requested and sent: {file_path_to_read}")
                        logging.info(f"File read and appended to conversation: {file_path_to_read}")
                    else:
                        logging.warning("READ_A_FILE command received but file path not provided")

                # Process a file update
                elif llm_response.startswith("WRITE_A_FILE"):
                    lines = llm_response.split('\n', 2)
                    if len(lines) >= 3:
                        file_path_to_write = lines[1].strip()
                        file_contents_to_write = lines[2]
                        if write_file(file_path_to_write, file_contents_to_write):
                            updated_conversation = f"{conversationPlusResponse}\n\n{file_path_to_write}\n{file_contents_to_write}"
                            write_file("avatar/avatarConversation.txt", updated_conversation)
                            print(f"WRITE_A_FILE requested and written: {file_path_to_write}")
                            logging.info(f"File written: {file_path_to_write}")
                        else:
                            logging.error(f"Failed to write file: {file_path_to_write}")
                    else:
                        logging.warning("WRITE_A_FILE command received but file path or content not provided")

                # Extract response to developer
                elif llm_response.startswith("RESPOND_TO_DEVELOPER"):
                    responseToDeveloper = llm_response.split('\n', 1)[1] if '\n' in llm_response else ""
                    write_file("avatar/avatarResponseToDeveloper.md", responseToDeveloper)
                    updated_conversation = f"{conversationPlusResponse}\n\nRESPOND_TO_DEVELOPER:\n{responseToDeveloper}"
                    write_file("avatar/avatarConversation.txt", updated_conversation)
                    logging.info("Response to developer written")
                    break  # Exit the LLM loop as we have a response

                else:
                    # If no specific command is recognized, continue the conversation
                    logging.info("Continuing conversation with LLM")
                    continue

            except Exception as e:
                logging.error(f"Error in LLM interaction: {str(e)}")
                print(f"An error occurred: {str(e)}")
                break

        else:
            # This block executes if the for loop completes without breaking
            final_response = "Sorry, the LLM we queried was unable to successfully complete the task. Let's try again, or consider using another model."
            avatar_conversation = read_file("avatar/avatarConversation.txt")
            write_file("avatar/avatarConversation.txt", f"{avatar_conversation}\n\n{final_response}")
            print(final_response)
            logging.warning("LLM failed to complete task within maximum iterations")

        # notify the developer
        print("\nAvatar response saved to avatar/avatarResponseToDeveloper.md")
        print("\nReady for next input. Type 'avatar down' to exit.")
        logging.info("Avatar ready for next input")

if __name__ == "__main__":
    main()