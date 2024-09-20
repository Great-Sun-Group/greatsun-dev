from utils.file_operations import read_file, write_file, get_directory_tree, install_package
from utils.git_operations import execute_git_command, create_branches, checkout_branches, push_changes, merge_to_dev
from utils.responseParser import parse_llm_response
import sys
import logging
import os
import json
import subprocess
import uuid
import site
import importlib.util
from typing import Optional
import time

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

# Add user site-packages to Python path
user_site_packages = site.getusersitepackages()
sys.path.append(user_site_packages)

# Check if anthropic is installed, if not, install it
if importlib.util.find_spec("anthropic") is None:
    print("anthropic package not found. Attempting to install...")
    if not install_package("anthropic"):
        print("Failed to install anthropic. Please install it manually and try again.")
        sys.exit(1)

# Now try to import anthropic
try:
    print("Attempting to import anthropic...")
    import anthropic
    print(f"anthropic module found at: {anthropic.__file__}")
    from anthropic import Anthropic
    print("Successfully imported Anthropic")
except ImportError as e:
    print(f"Error importing Anthropic: {e}")
    print("Trying to get more information about the package:")
    try:
        import pkg_resources
        anthropic_dist = pkg_resources.get_distribution("anthropic")
        print(f"Anthropic version: {anthropic_dist.version}")
        print(f"Anthropic location: {anthropic_dist.location}")
    except Exception as pkg_error:
        print(f"Error getting package information: {pkg_error}")
    sys.exit(1)


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

# Git operation functions

def main():
    ANTHROPIC_API_KEY = os.environ.get('CLAUDE')
    GH_USERNAME = os.environ.get('GH_USERNAME')
    MAX_LLM_ITERATIONS = 14
    MODEL_NAME = "claude-3-sonnet-20240229"
    SYSTEM_PROMPT = read_file("avatar/context/response_instructions.txt")

    try:
        logger.info("Starting avatar environment")
        large_language_model = Anthropic(api_key=ANTHROPIC_API_KEY)
        greatsun_developer = GH_USERNAME
    except Exception as e:
        logger.error(f"Failed to initialize Anthropic client: {str(e)}")
        print(f"Error initializing Anthropic client: {e}")
        return

# Prepare the initial context
    avatarUp_content = [
        read_file("avatar/context/avatar_orientation.md"),
        read_file("avatar/context/response_instructions.txt"),
        "** This is the project README.md **",
        read_file("README.md"),
        "** This is the credex-core submodule README.md **",
        read_file("credex-ecosystem/credex-core/README.md"),
        "** This is the vimbiso-pay submodule README.md **",
        read_file("credex-ecosystem/vimbiso-pay/README.md"),
        "** This is the current project **",
        read_file("avatar/context/current_project.md"),
        "** This is the full project structure **",
        json.dumps(get_directory_tree('/workspaces/greatsun-dev'), indent=2),
        "** INITIAL DEVELOPER INSTRUCTIONS **",
    ]
    conversation_thread = "\n\n".join(avatarUp_content)
    write_file("avatar/context/conversation_thread.txt", conversation_thread)
    logger.info("Initial context prepared")
    clear_screen()

    print("@greatsun-dev: welcome to your development environment. how can I help you?")

    while True:
        terminal_input = input(f"@{greatsun_developer}: ").strip()

        if terminal_input.lower() == "avatar down":
            print("greatsun-dev avatar, signing off")
            break

        if terminal_input.lower() == "avatar commit":
            try:
                commit_message = input("Enter commit message: ")
                if push_changes(commit_message):
                    write_file("avatar/context/conversation_thread.txt",
                               "ready for conversation")
                    logger.info(f"Commit made and avatar cleared")
                    print(f"Commit made and avatar cleared")
                else:
                    print("Failed to perform commit. Check logs for details.")
                continue
            except Exception as e:
                logger.error(f"Failed to perform cross-repo commit: {str(e)}")
                print("Failed to perform commit. Check logs for details.")
                continue

        if terminal_input.lower().startswith("avatar create branch"):
            branch_name = terminal_input.split(
                "avatar create branch", 1)[1].strip()
            if create_branches(branch_name):
                print(f"Created and checked out new branch '{
                      branch_name}' in all repos")
            else:
                print(f"Failed to create branch '{
                      branch_name}'. Check logs for details.")
            continue

        if terminal_input.lower().startswith("avatar checkout"):
            branch_name = terminal_input.split("avatar checkout", 1)[1].strip()
            if checkout_branches(branch_name):
                print(f"Checked out branch '{branch_name}' in all repos")
            else:
                print(f"Failed to checkout branch '{
                      branch_name}'. Check logs for details.")
            continue

        if terminal_input.lower() == "avatar merge to dev":
            if merge_to_dev():
                print("Successfully merged changes to dev branch in all repos")
            else:
                print("Failed to merge changes to dev. Check logs for details.")
            continue

        if terminal_input.lower() == "avatar clear":
            conversation_thread = "\n\n".join(avatarUp_content)
            write_file("avatar/context/conversation_thread.txt",
                       conversation_thread)
            logger.info(
                "Avatar conversation cleared and reset to initial context")
            clear_screen()
            print("Conversation cleared and reset to initial context")
            continue

        # Add new terminal message to conversation
        conversation_thread = read_file(
            "avatar/context/conversation_thread.txt")
        conversation_thread += f"\n\n*** DEVELOPER INPUT ***\n\n{
            terminal_input}"
        write_file("avatar/context/conversation_thread.txt",
                   conversation_thread)

        # START LLM LOOP, allow to run up to MAX_LLM_ITERATIONS iterations
        for iteration in range(MAX_LLM_ITERATIONS):
            try:
                llm_message = conversation_thread
                logger.info(
                    f"Sending message to LLM (iteration {iteration + 1})")
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
                conversation_thread += f"\n\n*** LLM RESPONSE ***\n\n{
                    llm_response}"
                logger.info("Received response from LLM")

                # Process the LLM response
                conversation_thread, developer_input_required, terminal_output = parse_llm_response(
                    conversation_thread, llm_response)
                write_file("avatar/context/conversation_thread.txt",
                           conversation_thread)

                print(terminal_output)

                if developer_input_required:
                    logger.info(
                        "Developer input required. Waiting for response.")
                    print(
                        "\nDeveloper input required. Please provide your next instruction.")
                    break

                # If no developer input is required, but there's no more to do, also break
                if not terminal_output.strip():
                    logger.info(
                        "No more actions to perform. Waiting for next instruction.")
                    print(
                        "\nNo more actions to perform. Please provide your next instruction.")
                    break

                # If there are more actions to perform, continue to the next iteration
                print("Continuing to next iteration")
                logger.info("Continuing to next iteration")

            except anthropic.APIError as e:
                logger.error(f"Anthropic API error in LLM iteration {
                             iteration + 1}: {str(e)}")
                print(f"An error occurred with the Anthropic API in LLM iteration {
                      iteration + 1}:")
                print(str(e))
                print("Please check the logs for more details.")
                break
            except Exception as e:
                logger.error(f"Error in LLM iteration {
                             iteration + 1}: {str(e)}")
                print(f"An unexpected error occurred in LLM iteration {
                      iteration + 1}:")
                print(str(e))
                print("Please check the logs for more details.")
                break

        else:
            # This block executes if the for loop completes without breaking
            final_response = "The LLM reached the maximum number of iterations without completing the task. Let's try again or consider rephrasing the request."
            logger.warning("LLM reached maximum iterations without completion")
            conversation_thread += f"\n\n{final_response}"
            write_file("avatar/context/conversation_thread.txt",
                       conversation_thread)
            print(final_response)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nOperation interrupted by user. Exiting gracefully.")
    except Exception as e:
        logger.critical(f"Critical error in main execution: {str(e)}")
        print("A critical error occurred in the main execution:")
        print(str(e))
        print("Please check the logs for more details.")
