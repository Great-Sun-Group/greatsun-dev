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

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def main():
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

    first_run = True
    logger.info("Starting avatar environment")
    # Clear the context
    write_file("avatar/avatarConversation.txt", "ready for conversation")

    clear_screen()
    print("Welcome to the greatsun-dev avatar environment.")
    print("The text in avatar/messageFromDeveloper.md will be appended to")
    print("your message below and sent to greatsun-dev")
    
    while True:
        if first_run or developer_input_required:
            terminal_input = input(f"{greatsun_developer}: ").strip()

            if terminal_input.lower() == "avatar down":
                write_file("avatar/avatarConversation.txt", "ready for conversation")
                logger.info("Avatar conversation cleared")
                logger.info("Avatar environment shutting down")
                print("\ngreatsun-dev avatar, signing off\n\n")
                break

            if terminal_input.lower() == "avatar commit":
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

            if terminal_input.lower() == "avatar clear":
                write_file("avatar/avatarConversation.txt", "ready for conversation")
                logger.info("Avatar conversation cleared")
                clear_screen()
                print("Conversation cleared")
                first_run = True
                continue

            # Prepare the message from the developer
            append_to_terminal_input = read_file("avatar/appendToTerminalInput.md")
            trigger_message_content = f"{terminal_input}\n\n{append_to_terminal_input}"

            if first_run:
                # Prepare the full context for the LLM (first run)
                avatar_up_content = [
                    read_file("avatar/avatarOrientation.md"),
                    read_file("avatar/responseInstructions.txt"),
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
                    "** INITIAL DEVELOPER INSTRUCTIONS **",
                    trigger_message_content
                ]
                conversation_thread = "\n\n".join(avatar_up_content)
                first_run = False
                logger.info("First run context prepared")
            else:
                # Add new terminal message to conversation
                conversation_thread = f"{conversation_thread}\n\n*** DEVELOPER INSTRUCTIONS ***\n\n{trigger_message_content}\n"

        # START LLM LOOP, allow to run up to MAX_LLM_ITERATIONS iterations
        for iteration in range(MAX_LLM_ITERATIONS):
            try:
                llm_message = conversation_thread
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
                conversation_thread = f"{conversation_thread}\n\n*** LLM RESPONSE ***\n\n{llm_response}"
                logger.info("Received response from LLM")

                # Process the LLM response
                conversation_thread, developer_input_required = parse_llm_response(conversation_thread, llm_response)
                print(conversation_thread)

                # If developer input is required, save conversation thread and break the loop
                if developer_input_required:
                    write_file("avatar/avatarConversation.txt", conversation_thread)
                    logger.info("Developer input required. Waiting for response.")
                    print("\nDeveloper input required. Please provide your next instruction.")
                    break

                # Else continue to the next iteration of the loop
                print("Continuing to next iteration")
                logger.info("Continuing to next iteration")

            except Exception as e:
                logger.error(f"Error in LLM iteration {iteration + 1}: {str(e)}")
                print(f"An error occurred in LLM iteration {iteration + 1}:")
                print(str(e))
                print("Please check the logs for more details.")
                developer_input_required = True
                break
        else:
            # This block executes if the for loop completes without breaking
            final_response = "The LLM reached the maximum number of iterations without completing the task. Let's try again or consider rephrasing the request."
            logger.warning("LLM reached maximum iterations without completion")
            write_file("avatar/avatarConversation.txt", f"{conversation_thread}\n\n{final_response}")
            print(final_response)
            developer_input_required = True

        if not developer_input_required:
            # If no developer input is required, continue the loop
            continue

        # Notify the developer
        print("\ngreatsun-dev is waiting for your next response")
        print("Enter your response below, or use one of the following commands:")
        print("'avatar down' to exit, 'avatar clear' to start a new conversation, 'avatar commit' to commit changes")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logger.critical(f"Critical error in main execution: {str(e)}")
        print("A critical error occurred in the main execution:")
        print(str(e))
        print("Please check the logs for more details.")