import os
import sys
import json
import time
import uuid
import shutil
import subprocess
from pathlib import Path
from typing import Tuple, Dict, Any

import site
import re
from github import Github, GithubException
from coolname import generate_slug
from anthropic import Anthropic

# For API communications between dev instances
# Replace https://localhost:port with respective codespaces url for codespaces
os.environ['CREDEX_CORE_API_URL'] = 'https://localhost:5000/api/v1 '
os.environ['VIMBISO_PAY_API_URL'] = 'https://localhost:8000/??? '

# Add user site-packages to Python path
user_site_packages = site.getusersitepackages()
sys.path.append(user_site_packages)

# Configuration
BASE_DIR = Path('/workspaces/greatsun-dev')
MAX_LLM_ITERATIONS = 14
MODEL_NAME = "claude-3-sonnet-20240229"

# GitHub configuration
GH_USERNAME = os.environ.get('GH_USERNAME')
GH_PAT = os.environ.get('GH_PAT')
GH_ORGANIZATION = 'Great-Sun-Group'

# Repository structure
ROOT_REPO = 'greatsun-dev'
MODULE_FOLDER = 'credex-ecosystem'
SUBMODULES = ['credex-core', 'vimbiso-pay']

# Paths
ROOT_PATH = os.getcwd()
MODULE_PATH = os.path.join(ROOT_PATH, MODULE_FOLDER)

# Initialize Github client and Anthropic client
g = Github(GH_PAT)
LARGE_LANGUAGE_MODEL = Anthropic(api_key=os.environ.get('CLAUDE'))

# File operations


def read_file(file_path: Path) -> str:
    try:
        return file_path.read_text()
    except FileNotFoundError:
        return f"File not found: {file_path}"
    except Exception as e:
        return f"Error reading file: {str(e)}"


def write_file(file_path: Path, file_content: str) -> bool:
    try:
        file_path.parent.mkdir(parents=True, exist_ok=True)
        with file_path.open('w') as file:
            file.write(file_content)
        return True
    except Exception as e:
        print(f"Error writing to file {file_path}: {str(e)}")
        return False

# LLM response parsing and file operations


def parse_llm_response(llm_response: str, conversation_thread: str) -> Tuple[bool, str]:
    patterns = {
        'read': r'<read\s+path=(?:")?([^">]+)(?:")?\s*/>',
        'write': r'<write\s+path=(?:")?([^">]+)(?:")?>\s*([\s\S]*?)\s*</write>',
        'append': r'<append\s+path=(?:")?([^">]+)(?:")?>\s*([\s\S]*?)\s*</append>',
        'delete': r'<delete\s+path=(?:")?([^">]+)(?:")?\s*/>',
        'rename': r'<rename\s+current_path=(?:")?([^">]+)(?:")?(?:\s+new_path=(?:")?([^">]+)(?:")?)?\s*/>',
        'move': r'<move\s+current_path=(?:")?([^">]+)(?:")?(?:\s+new_path=(?:")?([^">]+)(?:")?)?\s*/>',
        'list_directory': r'<list_directory\s+path=(?:")?([^">]+)(?:")?\s*/>',
        'create_directory': r'<create_directory\s+path=(?:")?([^">]+)(?:")?\s*/>'
    }

    file_operation_performed = False


    for op, pattern in patterns.items():
        matches = re.findall(pattern, llm_response)
        for match in matches:
            file_operation_performed = True
            if op in ['read', 'delete', 'list_directory', 'create_directory']:
                path = match if isinstance(match, str) else match[0]
                result = perform_file_operation(op, path)
            elif op in ['write', 'append']:
                path, content = match
                result = perform_file_operation(op, path, content)
            elif op in ['rename', 'move']:
                current_path, new_path = match
                result = perform_file_operation(
                    op, current_path, new_path=new_path)
            conversation_thread += f"Operation: {
                op}\nArguments: {match}\nResult: {result}\n\n"

    return not file_operation_performed, conversation_thread

def perform_file_operation(operation: str, path: str, content: str = None, new_path: str = None) -> str:
    full_path = Path(path) if Path(path).is_absolute() else BASE_DIR / path

    try:
        if operation == 'read':
            with open(full_path, 'r') as file:
                return f"File contents:\n{file.read()}"
        elif operation == 'write':
            full_path.parent.mkdir(parents=True, exist_ok=True)
            with open(full_path, 'w') as file:
                file.write(content)
            return f"File written successfully: {full_path}"
        elif operation == 'append':
            with open(full_path, 'a') as file:
                file.write(content)
            return f"Content appended successfully to: {full_path}"
        elif operation == 'delete':
            if full_path.is_file():
                os.remove(full_path)
                return f"File deleted successfully: {full_path}"
            elif full_path.is_dir():
                shutil.rmtree(full_path)
                return f"Directory deleted successfully: {full_path}"
            else:
                return f"Path not found: {full_path}"
        elif operation in ['rename', 'move']:
            new_full_path = Path(new_path) if Path(new_path).is_absolute() else BASE_DIR / new_path
            new_full_path.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(full_path, new_full_path)
            return f"{'Renamed' if operation == 'rename' else 'Moved'} successfully: {full_path} -> {new_full_path}"
        elif operation == 'list_directory':
            if full_path.is_dir():
                return f"Directory contents of {full_path}:\n" + "\n".join(str(item) for item in full_path.iterdir())
            else:
                return f"Not a directory: {full_path}"
        elif operation == 'create_directory':
            full_path.mkdir(parents=True, exist_ok=True)
            return f"Directory created successfully: {full_path}"
        else:
            return f"Unknown operation: {operation}"
    except Exception as e:
        return f"Error performing {operation} on {path}: {str(e)}"

# Directory tree generation


def get_directory_tree(path: Path) -> Dict[str, Any]:
    tree = {}
    excluded_files = {'.DS_Store', 'Thumbs.db', '.gitignore', '.gitattributes', '.env', '.coverage',
                      '*.pyc', '*.pyo', '*.whl', '*.egg', '*.log', '*.zip', '*.tar.gz', '*.rar', '*.db', '*.sqlite'}
    excluded_dirs = {'__pycache__', '.git', '.svn', '.hg', 'node_modules', 'venv',
                     'env', 'build', 'dist', '.vscode', '.idea', 'tmp', 'temp', 'htmlcov'}

    try:
        for entry in path.iterdir():
            if entry.is_dir():
                if entry.name in excluded_dirs or entry.name.endswith('.egg-info'):
                    continue
                subtree = get_directory_tree(entry)
                if subtree:  # Only add non-empty directories
                    tree[entry.name] = subtree
            elif entry.is_file():
                if any(entry.name.endswith(ext) for ext in excluded_files):
                    continue
                tree[entry.name] = None
    except Exception as e:
        print(f"Error getting directory tree for {path}: {str(e)}")

    return tree

# Context loading


def load_initial_context() -> str:
    initial_context = [
        read_file(BASE_DIR / "avatar/context/avatar_orientation.md"),
        read_file(BASE_DIR / "avatar/utils/response_instructions.txt"),
        f"\n\n*** README.md ***\n\n",
        read_file(BASE_DIR / "README.md"),
        f"\n\n*** credex-core/README.md ***\n\n",
        read_file(BASE_DIR / "credex-ecosystem/credex-core/README.md"),
        f"\n\n*** credex-ecosystem/vimbiso-pay/README.md ***\n\n",
        read_file(BASE_DIR / "credex-ecosystem/vimbiso-pay/README.md"),
        f"*** FULL DIRECTORY TREE ***\n\n",
        json.dumps(get_directory_tree(BASE_DIR), indent=2),
        f"\n\n*** avatar/context/current_project.md ***\n\n",
        read_file(BASE_DIR / "avatar/context/current_project.md"),
        f"\n\n*** MESSAGE FROM DEVELOPER @{
            os.environ.get('GH_USERNAME')} ***\n\n",
    ]
    return ''.join(initial_context)

# Git operations


def get_repo(repo_name):
    return g.get_repo(f"{GH_ORGANIZATION}/{repo_name}")


def get_current_branch(repo_path=None):
    original_dir = os.getcwd()
    try:
        if repo_path:
            os.chdir(repo_path)
        current_branch = subprocess.check_output(['git', 'rev-parse', '--abbrev-ref', 'HEAD'],
                                                 stderr=subprocess.DEVNULL).decode().strip()
        return current_branch
    except subprocess.CalledProcessError:
        print(f"Failed to get current branch for {
              repo_path or 'current directory'}. Are you in a Git repository?")
        return None
    finally:
        os.chdir(original_dir)


def get_off_dev_and_project_branch():
    current_branch = get_current_branch()
    if current_branch == 'dev' or current_branch.endswith('-project'):
        new_branch = f"avatar-{generate_slug(2)}"

        try:
            subprocess.run(['git', 'checkout', '-b', new_branch],
                           check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            print(f"on branch {new_branch}")
        except subprocess.CalledProcessError:
            print(f"Failed to create and switch to new branch: {new_branch}")
            return current_branch

        repo = get_repo(ROOT_REPO)
        try:
            repo.create_git_ref(
                f"refs/heads/{new_branch}", repo.get_branch("dev").commit.sha)
        except Exception as e:
            print(f"Failed to create new branch in GitHub repo: {str(e)}")

        return new_branch
    else:
        print(f"on branch {current_branch}")
        return current_branch


def load_project_git(load_branch):
    current_branch = get_current_branch()
    print(f"Current branch: {current_branch}")
    os.makedirs(MODULE_PATH, exist_ok=True)
    os.chdir(ROOT_PATH)

    # Recreate .gitmodules file
    gitmodules_path = os.path.join(ROOT_PATH, '.gitmodules')
    print("Recreating .gitmodules file")
    with open(gitmodules_path, 'w') as f:
        for submodule in SUBMODULES:
            f.write(f"[submodule \"credex-ecosystem/{submodule}\"]\n")
            f.write(f"\tpath = credex-ecosystem/{submodule}\n")
            f.write(
                f"\turl = https://github.com/Great-Sun-Group/{submodule}.git\n\n")

    # Remove existing submodules
    subprocess.run(['git', 'submodule', 'deinit', '-f', '--all'], check=True)

    # Initialize submodules
    subprocess.run(['git', 'submodule', 'init'], check=True)

    for submodule in SUBMODULES:
        submodule_dir = os.path.join(MODULE_PATH, submodule)
        print(f"Processing submodule: {submodule}")
        submodule_repo = get_repo(submodule)
        clone_url = submodule_repo.clone_url.replace(
            'https://', f'https://{GH_USERNAME}:{GH_PAT}@')

        if os.path.exists(submodule_dir):
            shutil.rmtree(submodule_dir)

        print(f"Cloning {submodule}...")
        os.chdir(MODULE_PATH)
        subprocess.run(['git', 'clone', '-b', load_branch,
                       clone_url, submodule], check=True)

        os.chdir(submodule_dir)
        subprocess.run(['git', 'checkout', load_branch], check=True)
        subprocess.run(['git', 'pull', 'origin', load_branch], check=True)

        print(f"Updated {submodule}")
        os.chdir(ROOT_PATH)

    print(f"Submodules synced to {load_branch}")

    conversation_thread = load_initial_context()
    write_file(BASE_DIR / "avatar/conversation_thread.txt",
               conversation_thread)
    print(f"Submodules in {current_branch} synced to {load_branch}")


def has_staged_changes(repo_path):
    original_dir = os.getcwd()
    try:
        os.chdir(repo_path)
        result = subprocess.run(['git', 'diff', '--staged', '--quiet'],
                                capture_output=True, text=True)
        return result.returncode == 1
    except subprocess.CalledProcessError as e:
        print(f"Git command error in {repo_path}: {e}")
        return False
    except Exception as e:
        print(f"An error occurred in {repo_path}: {e}")
        return False
    finally:
        os.chdir(original_dir)


def avatar_commit_git():
    commit_message = input("Enter commit message: ")
    changes_found = False
    commit_id = str(uuid.uuid4())
    full_commit_message = f"{commit_message}\n\nCommit-ID: {commit_id}"

    repos = [ROOT_REPO] + SUBMODULES
    repo_changes = {}

    current_branch = get_current_branch()

    # First, check for changes and store them
    for repo_name in repos:
        repo_path = ROOT_PATH if repo_name == ROOT_REPO else os.path.join(
            MODULE_PATH, repo_name)
        os.chdir(repo_path)

        if has_staged_changes(repo_path):
            changes_found = True
            repo_changes[repo_name] = repo_path

            # If it's a submodule, check if the branch exists and create it if it doesn't
            if repo_name != ROOT_REPO:
                try:
                    subprocess.run(['git', 'rev-parse', '--verify', current_branch],
                                   check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                except subprocess.CalledProcessError:
                    # Branch doesn't exist, so create it
                    subprocess.run(
                        ['git', 'checkout', '-b', current_branch], check=True)
                    print(f"Created and switched to branch {
                          current_branch} in {repo_name}")
                else:
                    # Branch exists, so just switch to it
                    subprocess.run(
                        ['git', 'checkout', current_branch], check=True)
                    print(f"Switched to existing branch {
                          current_branch} in {repo_name}")

    if not changes_found:
        print("No changes to commit in any repository.")
        return

    # If changes are found, commit them with the same message and timestamp
    commit_timestamp = int(time.time())
    for repo_name, repo_path in repo_changes.items():
        os.chdir(repo_path)

        # Set the commit timestamp
        os.environ['GIT_AUTHOR_DATE'] = str(commit_timestamp)
        os.environ['GIT_COMMITTER_DATE'] = str(commit_timestamp)

        try:
            # Commit the changes
            subprocess.run(
                ['git', 'commit', '-m', full_commit_message], check=True, env=os.environ)

            print(f"Changes committed locally in {
                  repo_name} on {current_branch}")
        except subprocess.CalledProcessError as e:
            print(f"Error in {repo_name}: {e}")

    os.chdir(ROOT_PATH)


def avatar_submit_git(project_branch):
    if (project_branch == "dev"):
        print("`dev` is not a project")
        return
    if not project_branch.endswith('-project'):
        project_branch = f"{project_branch}-project"

    repos = [ROOT_REPO] + SUBMODULES
    current_branch = get_current_branch()

    for repo_name in repos:
        repo_path = ROOT_PATH if repo_name == ROOT_REPO else os.path.join(
            MODULE_PATH, repo_name)
        os.chdir(repo_path)

        # 1. Push local changes to remote
        try:
            subprocess.run(
                ['git', 'push', 'origin', current_branch], check=True)
            print(f"Changes pushed in {repo_name} on branch {current_branch}")
        except subprocess.CalledProcessError as e:
            print(f"Error pushing changes in {repo_name}: {e}")
            continue

        # Get the GitHub repo object
        gh_repo = get_repo(repo_name)

        # 2. Check if remote branch project_branch exists
        try:
            gh_repo.get_branch(project_branch)
            branch_exists = True
        except GithubException:
            branch_exists = False

        if not branch_exists:
            # 2a. If no, create and merge local_branch into project_branch
            try:
                # Create the new branch
                sb = gh_repo.get_branch(current_branch)
                gh_repo.create_git_ref(
                    ref=f'refs/heads/{project_branch}', sha=sb.commit.sha)

                # Merge local_branch into project_branch
                gh_repo.merge(project_branch, current_branch, f"Merging {
                              current_branch} into {project_branch}")
                print(f"{current_branch} opens {
                      project_branch} in {repo_name}")
            except GithubException as e:
                print(f"Error creating/merging branch in {repo_name}: {e}")
        else:
            # 2b. If yes, create a pull request to merge local_branch to project branch
            try:
                pr_title = f"Merge {current_branch} into {project_branch}"
                pr_body = f"Automated pull request to merge changes from {
                    current_branch} into {project_branch}"
                gh_repo.create_pull(
                    title=pr_title, body=pr_body, head=current_branch, base=project_branch)
                print(f"{current_branch} submitted to {
                      project_branch} in {repo_name}")
            except GithubException as e:
                print(f"Error creating pull request in {repo_name}: {e}")

    os.chdir(ROOT_PATH)


def main():
    print(f"\n@greatsun-dev reading you loud and clear")
    get_off_dev_and_project_branch()
    conversation_thread = read_file(
        BASE_DIR / "avatar/conversation_thread.txt")
    print(f"\n*** MESSAGE FROM DEVELOPER @{GH_USERNAME} ***\n")

    while True:
        terminal_input = input().strip()

        if terminal_input.lower() == "avatar refresh":
            conversation_thread = load_initial_context()
            write_file(BASE_DIR / "avatar/conversation_thread.txt",
                       conversation_thread)
            print(f"*** MESSAGE FROM DEVELOPER @{GH_USERNAME} ***\n")
            continue

        if terminal_input.lower() == "avatar load":
            load_branch = input("Project branch or `dev`: ")
            try:
                load_project_git(load_branch)
            except Exception as e:
                print(f"Error loading project: {str(e)}")
                print("Traceback:")
                import traceback
                traceback.print_exc()
            continue


        if terminal_input.lower() == "avatar engage":

            # Fire up credex-core
            '''
            os.chdir('/workspaces/greatsun-dev/credex-ecosystem/credex-core')
            subprocess.run(['docker', 'build', '-t', 'credex-core', '.'], check=True)
            env_vars = subprocess.check_output(
                "env | grep -v ' '", shell=True).decode('utf-8')
            docker_run_cmd = [
                'docker', 'run',
                '-p', '5000:5000',
                '--env', f'NODE_ENV=development',
                '--env-file', '/dev/stdin',
                '--name', 'credex-core',
                'credex-core'
            ]
            subprocess.run(docker_run_cmd, input=env_vars.encode(), check=True)
            '''


            # Change directory to vimbiso-pay/app
            os.chdir('/workspaces/greatsun-dev/credex-ecosystem/vimbiso-pay/app')

            # Remove any existing containers with the name "vimbiso-pay"
            containers = subprocess.check_output(
                ['docker', 'ps', '-q', '-a']).decode().strip().split('\n')
            vimbiso_pay_container = [c for c in containers if 'vimbiso-pay' in subprocess.check_output(
                ['docker', 'inspect', '--format', '{{.Name}}', c]).decode().strip()]
            if vimbiso_pay_container:
                subprocess.run(
                    ['docker', 'rm', '-f', vimbiso_pay_container[0]], check=True)

            # Build the Docker image
            subprocess.run(['docker', 'build', '-t', 'vimbiso-pay', '.'], check=True)

            # Run the Docker container
            env_vars = subprocess.check_output(
                "env | grep -v ' '", shell=True).decode('utf-8')
            docker_run_cmd = [
                'docker', 'run',
                '-p', '8000:8000',
                '--env-file', '/dev/stdin',
                '--name', 'vimbiso-pay',
                'vimbiso-pay',
                'python', 'manage.py', 'runserver', '0.0.0.0:8000'
            ]

            subprocess.run(docker_run_cmd, input=env_vars.encode(), check=True)

            continue

        if terminal_input.lower() == "avatar commit":
            avatar_commit_git()
            continue

        if terminal_input.lower() == "avatar submit":
            project_branch = input("Project branch: ")
            avatar_submit_git(project_branch)
            continue

        if terminal_input.lower() == "avatar down":
            current_branch = get_current_branch()
            print(f"\ngreatsun-dev signing off branch {current_branch}")
            break

        # Add new terminal message to conversation
        conversation_thread += f"\n\n*** MESSAGE FROM DEVELOPER @{
            GH_USERNAME} ***\n\n{terminal_input}"
        write_file(BASE_DIR / "avatar/conversation_thread.txt",
                   conversation_thread)

        # START LLM LOOP, allow to run up to MAX_LLM_ITERATIONS iterations
        for iteration in range(MAX_LLM_ITERATIONS):
            try:
                llm_message = conversation_thread
                print(f"avatar iteration {
                      iteration + 1} of up to {MAX_LLM_ITERATIONS}")


                llm_call = LARGE_LANGUAGE_MODEL.messages.create(
                    model=MODEL_NAME,
                    max_tokens=4096,
                    temperature=0,
                    system=read_file(
                        BASE_DIR / "avatar/utils/response_instructions.txt"),
                    messages=[
                        {"role": "user", "content": llm_message}
                    ]
                )
                llm_response = llm_call.content[0].text
                conversation_thread += f"\n\n*** LLM RESPONSE ***\n\n{
                    llm_response}\n\n*** AUTOMATED RESPONSE TO ANY FILE OPERATIONS REQUESTED ***\n\n"

                # Process the LLM response
                developer_input_required, updated_conversation_thread = parse_llm_response(
                    llm_response, conversation_thread)

                # Update conversation_thread with the result from parse_llm_response
                conversation_thread = updated_conversation_thread

                # Write the updated conversation thread to file
                write_file(BASE_DIR / "avatar/conversation_thread.txt",
                           conversation_thread)

                if developer_input_required:
                    print(f"\n*** MESSAGE FROM DEVELOPER @{GH_USERNAME} ***")
                    break

            except Exception as e:
                print(f"Error in LLM iteration {iteration + 1}: {str(e)}")
                print("Please check the logs for more details.")
                conversation_thread += f"\n\nError in LLM iteration {iteration + 1}: {str(e)}"
                write_file(BASE_DIR / "avatar/conversation_thread.txt", conversation_thread)
                break

        else:
            # This block executes if the for loop completes without breaking
            final_response = "The LLM reached the maximum number of iterations without completing the task. Let's try again or consider rephrasing the request."
            print("LLM reached maximum iterations without completion")
            conversation_thread += f"\n\n{final_response}"
            write_file(BASE_DIR / "avatar/conversation_thread.txt", conversation_thread)
            print(final_response)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nOperation interrupted by user. Exiting gracefully.")
    except Exception as e:
        print(f"Critical error in main execution: {str(e)}")
        print("A critical error occurred in the main execution:")
        print(str(e))
        print("Error type:", type(e).__name__)
        import traceback
        print("Traceback:")
        traceback.print_exc()