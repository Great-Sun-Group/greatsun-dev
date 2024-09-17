"""
## avatar/avatarUp.py
At the core of the avatar are the avatar/avatarUp.py and avatar/responseParser.py scripts that we are interacting through.
This script allows you to perform file operations within the project environment.
It is critical that you thoroughly review and understand these scripts, because to iterate with the script
**you must respond to this query in a format that the script can parse, with your requests at the end of your response.**
You need to understand this script in order to know how to respond in a way that will enable you to iterate operations and summarize your findings and actions in messages to the developer.

## Your response
The script will extract the patterns described below from your response. Using these patterns/commands will enable you to interact with the codebase. When you are finished your analysis and updates, respond to this message without any of the patterns, and the script will exit the loop and wait for developer input.

### Usage for iterations
If the script detects one of these patterns, it will carry out the requested action, append the results to this conversation thread, and return it to you. Requesting an action is the means to keep the script iterating. To finish your analysis and updates, provide a response without any of the operation patterns. This will signal the script to exit the loop and wait for developer input.

Note: If an operation fails (e.g., file not found), an error message will be returned. You should handle these errors appropriately in your subsequent responses.

Example of a complete response:
Based on my analysis of the current project structure, I suggest we read the contents of the main configuration file.

read_file/workspaces/greatsun-dev/config.json

***
and here are examples of the other functions you can access
***

write_file/path/here.py
[Content starts on the next line]
import json
import os

(Rest of the file contents here)
[Content ends before the next operation or end of message]

list_directory/path/here/

delete_file/path/here.py


rename_file/old/path/here.py
rename_file/new/path/here.py

move_file/current/path/here.py
move_file/new/path/here.py


***************************************************************

!!! IMPORTANT IMPORTANT IMPORTANT !!!

BELOW ARE THE SCRIPTS THAT WILL PROCESS YOUR RESPONSE.

The response formats described in English above are executed with this script. You must fully understand this script so that you can use the avatar to extend your capacity to act. Use the abilities offered by the avatar to implement the developer's intent.

!!! IMPORTANT IMPORTANT IMPORTANT !!!

***************************************************************
"""

import sys
import logging

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

from utils import read_file, write_file, get_directory_tree
from responseParser import parse_llm_response
from avatarUpCommands import cross_repo_commit
from anthropic import Anthropic
import os
import json

# Constants
ANTHROPIC_API_KEY = os.environ.get('CLAUDE')
GITHUB_USERNAME = os.environ.get('GITHUB_USERNAME')
MAX_LLM_ITERATIONS = 7
MODEL_NAME = "claude-3-5-sonnet-20240620"

# Initialize Anthropic client
try:
    large_language_model = Anthropic(api_key=ANTHROPIC_API_KEY)
    greatsun_developer = GITHUB_USERNAME
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
    print("Welcome to the greatsun-dev avatar environment")
    print("Enter your instructions or questions in avatar/messageFromDeveloper.md")
    print("Then press enter here in the terminal, or you can first")
    print("optionally paste a file path as a starting point for my work")
    print(f"{greatsun_developer}: ")

    while True:
        file_path = input().strip()

        if file_path.lower() == "avatar down":
            write_file("avatar/avatarConversation.txt",
                       "ready for conversation")
            logger.info("Avatar conversation cleared")
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
            logger.info("Avatar conversation cleared")
            print("Conversation cleared")
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
                "** This is avatar/avatarUp.py **",
                read_file("avatar/avatarUp.py"),
                "** This is avatar/responseParser.py **",
                read_file("avatar/responseParser.py"),
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
                print(f"Sending message to LLM (iteration {iteration + 1})")

                llm_call = large_language_model.messages.create(
                    model=MODEL_NAME,
                    max_tokens=4096,
                    messages=[
                        {"role": "user", "content": llm_message}
                    ]
                )
                llm_response = llm_call.content[0].text
                print("Received response from LLM:")
                print(llm_response)
                logger.info("Received response from LLM")

                # Process the LLM response
                processed_response, file_operation_performed = parse_llm_response(
                    llm_response)

                print("\nProcessed response:")
                print(processed_response)

                # Update conversation with processed response
                updated_conversation = f"{llm_message}\n\n{processed_response}"
                write_file("avatar/avatarConversation.txt",
                           updated_conversation)

                # Check if no file operations were performed
                if not file_operation_performed:
                    print("No file operations performed, exiting LLM loop")
                    logger.info(
                        "No file operations performed, exiting LLM loop")
                    print("\nAI response ready. Here's the final response:")
                    print(processed_response)
                    break

                # If file operations were performed, continue to the next iteration
                print("File operation performed, continuing to next iteration")
                logger.info(
                    "File operation performed, continuing to next iteration")

            except Exception as e:
                logger.error(
                    f"Error in LLM iteration {iteration + 1}: {str(e)}")
                print(f"An error occurred in LLM iteration {iteration + 1}:")
                print(str(e))
                print("Please check the logs for more details.")
                break
        else:
            # This block executes if the for loop completes without breaking
            final_response = "The LLM reached the maximum number of iterations without completing the task. Let's try again or consider rephrasing the request."
            logger.warning("LLM reached maximum iterations without completion")
            avatar_conversation = read_file("avatar/avatarConversation.txt")
            write_file("avatar/avatarConversation.txt",
                       f"{avatar_conversation}\n\n{final_response}")
            print(final_response)

        # Notify the developer
        print("\ngreatsun-dev is waiting for your next response")
        print("Enter it in the messageFromDeveloper.md file and press enter here")
        print("or 'avatar down' to exit, 'avatar clear' to start a new conversation")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logger.critical(f"Critical error in main execution: {str(e)}")
        print("A critical error occurred in the main execution:")
        print(str(e))
        print("Please check the logs for more details.")
