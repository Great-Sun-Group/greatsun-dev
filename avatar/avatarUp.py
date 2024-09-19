from utils.file_operations import read_file, write_file, get_directory_tree
from utils.responseParser import parse_llm_response
import sys
import logging
import os
import json
import subprocess
import uuid
import site
import importlib.util
from typing import Tuple, List

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

# Diagnostic information
print(f"Python version: {sys.version}")
print(f"Python executable: {sys.executable}")
print(f"User site-packages: {user_site_packages}")
print(f"Python path: {sys.path}")


def install_package(package_name: str) -> bool:
    try:
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", package_name])
        print(f"Successfully installed {package_name}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Failed to install {package_name}: {e}")
        return False


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

# Import other required modules


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

# Git operation functions


def execute_git_command(repo: str, command: str) -> bool:
    repo_dirs = {
        "greatsun-dev": "/workspaces/greatsun-dev",
        "credex-core": "/workspaces/greatsun-dev/credex-ecosystem/credex-core",
        "vimbiso-pay": "/workspaces/greatsun-dev/credex-ecosystem/vimbiso-pay"
    }

    if repo not in repo_dirs:
        logger.error(f"Unknown repository: {repo}")
        return False

    try:
        result = subprocess.run(
            command, cwd=repo_dirs[repo], shell=True, check=True, capture_output=True, text=True)
        logger.info(f"Git command executed successfully in {repo}: {command}")
        return True
    except subprocess.CalledProcessError as e:
        logger.error(f"Error executing git command in {repo}: {e}")
        return False


def create_branches(branch_name: str) -> bool:
    repos = ["greatsun-dev", "credex-core", "vimbiso-pay"]
    for repo in repos:
        if not execute_git_command(repo, f"git fetch --all"):
            return False
        if not execute_git_command(repo, f"git checkout -b {branch_name} origin/dev || git checkout -b {branch_name}"):
            return False
    return True


def checkout_branches(branch_name: str) -> bool:
    repos = ["greatsun-dev", "credex-core", "vimbiso-pay"]
    for repo in repos:
        if not execute_git_command(repo, f"git checkout {branch_name}"):
            return False
    return True


def push_changes(commit_message: str) -> bool:
    repos = ["greatsun-dev", "credex-core", "vimbiso-pay"]
    commit_uuid = str(uuid.uuid4())
    for repo in repos:
        if not execute_git_command(repo, "git add ."):
            return False
        if not execute_git_command(repo, f'git commit -m "{commit_message} [{commit_uuid}]"'):
            return False
        if not execute_git_command(repo, "git push origin HEAD"):
            return False
    return True


def merge_to_dev() -> bool:
    repos = ["greatsun-dev", "credex-core", "vimbiso-pay"]
    current_branch = subprocess.check_output(
        ["git", "rev-parse", "--abbrev-ref", "HEAD"], text=True).strip()

    for repo in repos:
        if not execute_git_command(repo, "git fetch origin"):
            return False
        if not execute_git_command(repo, "git checkout dev"):
            return False
        if not execute_git_command(repo, "git pull origin dev"):
            return False
        if not execute_git_command(repo, f"git merge {current_branch}"):
            print(f"Merge conflict in {
                  repo}. Please resolve conflicts manually and complete the merge.")
            return False
        if not execute_git_command(repo, "git push origin dev"):
            return False
        print(f"Changes merged to dev branch in {
              repo}. Please create a pull request manually if needed.")

    for repo in repos:
        if not execute_git_command(repo, f"git checkout {current_branch}"):
            return False

    return True


def process_llm_response(conversation_thread: str, llm_response: str, max_iterations: int = 5) -> Tuple[str, bool, str]:
    for iteration in range(max_iterations):
        conversation_thread, developer_input_required, terminal_output = parse_llm_response(
            conversation_thread, llm_response)

        if developer_input_required or not terminal_output.strip():
            return conversation_thread, developer_input_required, terminal_output

        # If there are more actions to perform, continue to the next iteration
        conversation_thread += f"\n\n*** LLM RESPONSE ***\n\n{llm_response}"
        write_file("avatar/context/conversation_thread.txt",
                   conversation_thread)

        try:
            llm_call = large_language_model.messages.create(
                model=MODEL_NAME,
                max_tokens=4096,
                temperature=0,
                system=SYSTEM_PROMPT,
                messages=[
                    {"role": "user", "content": conversation_thread}
                ]
            )
            llm_response = llm_call.content[0].text
        except Exception as e:
            logger.error(f"Error in LLM call: {str(e)}")
            return conversation_thread, True, f"An error occurred: {str(e)}"

    # If we've reached this point, we've hit the maximum number of iterations
    final_response = "The LLM reached the maximum number of iterations without completing the task. Let's try again or consider rephrasing the request."
    logger.warning("LLM reached maximum iterations without completion")
    conversation_thread += f"\n\n{final_response}"
    return conversation_thread, True, final_response


def main():
    ANTHROPIC_API_KEY = os.environ.get('CLAUDE')
    GH_USERNAME = os.environ.get('GH_USERNAME')
    MAX_LLM_ITERATIONS = 14
    MODEL_NAME = "claude-3-5-sonnet-20240620"

    response_instructions_path = "avatar/context/response_instructions.txt"
    if not os.path.exists(response_instructions_path):
        default_instructions = "You are an AI assistant helping with development tasks."
        with open(response_instructions_path, "w") as f:
            f.write(default_instructions)
        print(f"Created default {response_instructions_path}")

    SYSTEM_PROMPT = read_file(response_instructions_path)

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
                print(f"Failed to checkout branch '{branch_name}'. Check logs for details.")
            continue

        if terminal_input.lower() == "avatar merge to dev":
            if merge_to_dev():
                print("Successfully merged changes to dev branch in all repos")
            else:
                print("Failed to merge changes to dev. Check logs for details.")
            continue

        if terminal_input.lower() == "avatar clear":
            conversation_thread = "\n\n".join(avatarUp_content)
            write_file("avatar/context/conversation_thread.txt", conversation_thread)
            logger.info("Avatar conversation cleared and reset to initial context")
            clear_screen()
            print("Conversation cleared and reset to initial context")
            continue

        # Add new terminal message to conversation
        conversation_thread = read_file("avatar/context/conversation_thread.txt")
        conversation_thread += f"\n\n*** DEVELOPER INPUT ***\n\n{terminal_input}"
        write_file("avatar/context/conversation_thread.txt", conversation_thread)

        # Process LLM response
        try:
            llm_call = large_language_model.messages.create(
                model=MODEL_NAME,
                max_tokens=4096,
                temperature=0,
                system=SYSTEM_PROMPT,
                messages=[
                    {"role": "user", "content": conversation_thread}
                ]
            )
            llm_response = llm_call.content[0].text
            logger.info("Received initial response from LLM")

            conversation_thread, developer_input_required, terminal_output = process_llm_response(
                conversation_thread, llm_response, MAX_LLM_ITERATIONS)
            
            write_file("avatar/context/conversation_thread.txt", conversation_thread)
            print(terminal_output)

            if developer_input_required:
                logger.info("Developer input required. Waiting for response.")
                print("\nDeveloper input required. Please provide your next instruction.")

        except Exception as e:
            logger.error(f"Error in LLM processing: {str(e)}")
            print(f"An error occurred while processing the request:")
            print(str(e))
            print("Please check the logs for more details.")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logger.critical(f"Critical error in main execution: {str(e)}")
        print("A critical error occurred in the main execution:")
        print(str(e))
        print("Please check the logs for more details.")