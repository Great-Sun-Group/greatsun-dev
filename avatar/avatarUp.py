#!/usr/bin/env python3

import sys
import logging
import os
import json
from utils import read_file, write_file, get_directory_tree
from responseParser import parse_llm_response
from avatarUpCommands import cross_repo_commit
from anthropic import Anthropic

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("avatar.log"),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# Check if we can write to the log file
try:
    with open("avatar.log", "a") as f:
        f.write("Logging test\n")
except IOError as e:
    print(f"Unable to write to log file: {str(e)}")
    print("Please check file permissions and try again.")
    sys.exit(1)

# Constants
ANTHROPIC_API_KEY = os.environ.get('CLAUDE')
DEVELOPER_GITHUB_USERNAME = os.environ.get('DEVELOPER_GITHUB_USERNAME')
MAX_LLM_ITERATIONS = 7
MODEL_NAME = "claude-3-5-sonnet-20240620"
SYSTEM_PROMPT = read_file("responseInstructions.txt")

# Initialize Anthropic client
try:
    large_language_model = Anthropic(api_key=ANTHROPIC_API_KEY)
    greatsun_developer = DEVELOPER_GITHUB_USERNAME
except Exception as e:
    logger.error(f"Failed to initialize Anthropic client: {str(e)}")
    raise

def main():
    """
    Main function to run the avatar environment.
    """
    first_run = True
    logger.info("Starting avatar environment")

    os.system('cls' if os.name == 'nt' else 'clear')
    print("welcome to the greatsun-dev avatar environment.")
    print("the text in avatar/messageFromDeveloper.md will be appended to")
    print("your message below and sent to greatsun-dev")
    print(f"{greatsun_developer}: ")

    while True:
        file_path = input().strip()

        if file_path.lower() == "avatar down":
            write_file("avatar/avatarConversation.txt", "ready for conversation")
            logger.info("Avatar conversation cleared")
            logger.info("Avatar environment shutting down")
            print("\ngreatsun-dev avatar, signing off\n\n")
            break

        if file_path.lower() == "avatar commit":
            try:
                commit_id = cross_repo_commit()
                if commit_id:
                    write_file("avatar/avatarConversation.txt", "ready for conversation")
                    logger.info(f"Commit {commit_id} made and avatar cleared")
                    print(f"Commit {commit_id} made and avatar cleared")
                    continue
            except Exception as e:
                logger.error(f"Failed to perform cross-repo commit: {str(e)}")
                print("Failed to perform commit. Check logs for details.")
                continue

        if file_path.lower() == "avatar clear":
            write_file("avatar/avatarConversation.txt", "ready for conversation")
            logger.info("Avatar conversation cleared")
            print("Conversation cleared")
            first_run = True  # Reset the flag when clearing
            continue

        # Prepare the message from the developer
        message_from_developer = read_file("avatar/messageFromDeveloper.md")
        reference_file_content = read_file(file_path) if file_path else "No reference file provided."
        trigger_message_content = f"{message_from_developer}\n\nReference File: {file_path}\n\n{reference_file_content}"

        if first_run:
            # Prepare the full context for the LLM (first run)
            avatar_up_content = [
                read_file("avatar/avatarOrientation.md"),
                read_file("avatar/responseInstructions.txt"),
                """
                "** This is the avatar/avatarUp.py script that will process the interactive loop you can use **",
                read_file("avatar/avatarUp.py"),
                "** This is avatar/responseParser.py that will parse your responses **",
                read_file("avatar/responseParser.py"),
                """
                "** This is the project README.md **",
                read_file("README.md"),
                "** This is the credex-core submodule README.md **",
                read_file("credex-ecosystem/credex-core/README.md"),
                "** This is the vimbiso-pay submodule README.md **",
                read_file("credex-ecosystem/vimbiso-pay/README.md"),
                "** This is the current project **",
                read_file("avatar/currentProject.md"),
                "** This is the full project structure **",
                json.dumps(get_directory_tree('/workspaces/greatsun-dev'), indent=2),
                "** IMPORTANT IMPORTANT IMPORTANT: Current Instructions from Developer: the purpose of this conversation **",
                trigger_message_content,
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
                logger.info(f"Sending message to LLM (iteration {iteration + 1})")
                print(f"Sending message to LLM (iteration {iteration + 1})")

                llm_call = large_language_model.messages.create(
                    model=MODEL_NAME,
                    max_tokens=4096,
                    temperature=0,
                    system=SYSTEM_PROMPT,
                    messages=[
                        {"role": "user", "content": llm_message}
                    ]
                )
                llm_response = llm_call.content[0].text
                print("Received response from LLM:")
                print(llm_response)
                logger.info("Received response from LLM")

                # Process the LLM response
                response_to_developer, file_operation_performed = parse_llm_response(llm_response)

                print("\nResponse to developer:")
                print(response_to_developer)

                # Update conversation with response to developer
                updated_conversation = f"{llm_message}\n\n{response_to_developer}"
                write_file("avatar/avatarConversation.txt", updated_conversation)

                # Check if no file operations were performed
                if not file_operation_performed:
                    print("No file operations performed, exiting LLM loop")
                    logger.info("No file operations performed, exiting LLM loop")
                    break

                # If file operations were performed, continue to the next iteration
                print("File operation performed, continuing to next iteration")
                logger.info("File operation performed, continuing to next iteration")

            except Exception as e:
                logger.error(f"Error in LLM iteration {iteration + 1}: {str(e)}")
                print(f"An error occurred in LLM iteration {iteration + 1}:")
                print(str(e))
                print("Please check the logs for more details.")
                break
        else:
            # This block executes if the for loop completes without breaking
            final_response = "The LLM reached the maximum number of iterations without completing the task. Let's try again or consider rephrasing the request."
            logger.warning("LLM reached maximum iterations without completion")
            avatar_conversation = read_file("avatar/avatarConversation.txt")
            write_file("avatar/avatarConversation.txt", f"{avatar_conversation}\n\n{final_response}")
            print(final_response)

        # Notify the developer
        print("\ngreatsun-dev is waiting for your next response")
        print("enter it in the messageFromDeveloper.md file and press enter here")
        print("or 'avatar down' to exit, 'avatar clear' to start a new conversation")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logger.critical(f"Critical error in main execution: {str(e)}")
        print("A critical error occurred in the main execution:")
        print(str(e))
        print("Please check the logs for more details.")