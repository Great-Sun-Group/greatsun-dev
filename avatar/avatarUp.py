import json
import os
import logging
import re
from anthropic import Anthropic
from avatarUpCommands import cross_repo_commit
from utils import read_file, write_file, get_directory_tree

# Configure logging
logging.basicConfig(filename='avatar.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Constants
ANTHROPIC_API_KEY = os.environ.get('CLAUDE')
GITHUB_USERNAME = os.environ.get('GITHUB_USERNAME')
MAX_LLM_ITERATIONS = 42
MODEL_NAME = "claude-3-5-sonnet-20240620"

# Initialize Anthropic client
try:
    large_language_model = Anthropic(api_key=ANTHROPIC_API_KEY)
    greatsun_developer = GITHUB_USERNAME
except Exception as e:
    logger.error(f"Failed to initialize Anthropic client: {str(e)}")
    raise


def extract_file_operation(response, operation):
    """
    Extract file operation details from LLM response.
    
    Args:
    response (str): LLM response
    operation (str): Either 'READ_FILE' or 'WRITE_FILE'
    
    Returns:
    tuple: (file_path, file_contents) for WRITE_FILE, or (file_path, None) for READ_FILE
    """
    if operation == 'READ_FILE':
        pattern = r"READ_FILE\n(.*?)\n"
    elif operation == 'WRITE_FILE':
        pattern = r"WRITE_FILE\n(.*?)\n<--write_file_start-->\n(.*?)\n<--write_file_end-->"
    else:
        logger.error(f"Invalid operation: {operation}")
        return None, None

    match = re.search(pattern, response, re.DOTALL)
    if match:
        if operation == 'READ_FILE':
            return match.group(1), None
        else:
            return match.group(1), match.group(2)
    return None, None


def process_llm_response(llm_response):
    """
    Process the LLM response and perform file operations.
    
    Args:
    llm_response (str): Response from the LLM
    
    Returns:
    str: Processed response for the developer
    """
    read_path, _ = extract_file_operation(llm_response, 'READ_FILE')
    write_path, write_contents = extract_file_operation(
        llm_response, 'WRITE_FILE')

    conversation = read_file("avatar/avatarConversation.txt")

    if read_path:
        try:
            read_data = f"READ_FILE\n{read_path}\n{read_file(read_path)}"
            conversation += f"\n\n{read_data}"
            logger.info(f"Read file: {read_path}")
        except Exception as e:
            logger.error(f"Failed to read file {read_path}: {str(e)}")

    if write_path and write_contents:
        try:
            write_file(write_path, write_contents)
            conversation += f"\n\nWRITE_FILE\n{write_path}\n{write_contents}"
            logger.info(f"Wrote file: {write_path}")
        except Exception as e:
            logger.error(f"Failed to write file {write_path}: {str(e)}")

    write_file("avatar/avatarConversation.txt", conversation)

    # Remove file operation patterns from the response
    response_to_developer = re.sub(
        r"(READ_FILE|WRITE_FILE).*?(<--write_file_end-->)?", "", llm_response, flags=re.DOTALL)
    return response_to_developer.strip()


def main():
    """
    Main function to run the avatar environment.
    """
    first_run = True
    logger.info("Starting avatar environment")

    os.system('cls' if os.name == 'nt' else 'clear')
    print("Welcome to the greatsun-dev avatar environment")
    print("Enter your instructions or questions in avatar/messageFromDeveloper.md")
    print("Then press enter here in the terminal, or you can first")
    print("optionally paste a file path as a starting point for my work")
    print(f"{greatsun_developer}: ")

    while True:
        file_path = input().strip()

        if file_path.lower() == "avatar down":
            logger.info("Avatar environment shutting down")
            print("\ngreatsun-dev avatar, signing off\n\n")
            break

        if file_path.lower() == "avatar commit":
            try:
                commit_id = cross_repo_commit()
                if commit_id:
                    write_file("avatar/avatarConversation.txt",
                               "ready for conversation")
                    logger.info(f"Commit {commit_id} made and avatar cleared")
                    print(f"Commit {commit_id} made and avatar cleared")
                    continue
            except Exception as e:
                logger.error(f"Failed to perform cross-repo commit: {str(e)}")
                print("Failed to perform commit. Check logs for details.")
                continue

        if file_path.lower() == "avatar clear":
            write_file("avatar/avatarConversation.txt",
                       "ready for conversation")
            logger.info("Avatar cleared")
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
                "** This is the current project **",
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
            logger.info("First run context prepared")
        else:
            # For subsequent runs, append to existing conversation
            existing_conversation = read_file("avatar/avatarConversation.txt")
            updated_conversation = f"{existing_conversation}\n\n** New input from developer **\n\n{trigger_message_content}\n"
            write_file("avatar/avatarConversation.txt", updated_conversation)
            logger.info("Appended new input to existing conversation")

# START LLM LOOP, allow to run up to MAX_LLM_ITERATIONS iterations
        for iteration in range(MAX_LLM_ITERATIONS):
            try:
                llm_message = read_file("avatar/avatarConversation.txt")
                logger.info(
                    f"Sending message to LLM (iteration {iteration + 1})")

                llm_call = large_language_model.messages.create(
                    model=MODEL_NAME,
                    max_tokens=4096,
                    messages=[
                        {"role": "user", "content": llm_message}
                    ]
                )
                llm_response = llm_call.content[0].text
                logger.info("Received response from LLM")

                # Process the LLM response
                processed_response = process_llm_response(llm_response)

                # Update conversation with processed response
                updated_conversation = f"{llm_message}\n\n{processed_response}"
                write_file("avatar/avatarConversation.txt",
                           updated_conversation)

                # Check if the task is complete
                if "TASK_COMPLETE" in processed_response:
                    logger.info("Task completed successfully")
                    print("\nTask completed. Here's the final response:")
                    print(processed_response)
                    break

                # If not complete, continue to the next iteration
                logger.info("Task not complete, continuing to next iteration")

            except Exception as e:
                logger.error(
                    f"Error in LLM iteration {iteration + 1}: {str(e)}")
                print(f"An error occurred. Please check the logs for details.")
                break
        else:
            # This block executes if the for loop completes without breaking
            final_response = "Sorry, the LLM was unable to successfully complete the task within the maximum allowed iterations. Let's try again, or consider using another model."
            logger.warning(
                "LLM failed to complete task within maximum iterations")
            avatar_conversation = read_file("avatar/avatarConversation.txt")
            write_file("avatar/avatarConversation.txt",
                       f"{avatar_conversation}\n\n{final_response}")
            print(final_response)

        # Notify the developer
        print("\nReady for next input. Type 'avatar down' to exit.")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logger.critical(f"Critical error in main execution: {str(e)}")
        print("A critical error occurred. Please check the logs for details.")
