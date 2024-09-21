import uuid
import os
import subprocess
import time
from github import Github, InputGitTreeElement, GithubException
from coolname import generate_slug
from utils.file_operations import load_initial_context, write_file

# GitHub configuration
GH_USERNAME = os.environ.get('GH_USERNAME')
GH_PAT = os.environ.get('GH_PAT')

# Repository structure
ROOT_REPO = 'greatsun-dev'
MODULE_FOLDER = 'credex-ecosystem'
SUBMODULES = [
    'credex-core',
    'vimbiso-pay'
]

# Paths
ROOT_PATH = os.getcwd()
MODULE_PATH = os.path.join(ROOT_PATH, MODULE_FOLDER)

# Initialize Github client
g = Github(GH_PAT)


def get_repo(repo_name):
    return g.get_repo(f"Great-Sun-Group/{repo_name}")


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


def get_off_dev_branch():
    current_branch = get_current_branch()
    if current_branch == 'dev':
        new_slug = generate_slug(2)
        new_branch = f"avatar-of-{new_slug}"

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
    os.makedirs(MODULE_PATH, exist_ok=True)
    os.chdir(MODULE_PATH)

    for submodule in SUBMODULES:
        submodule_dir = os.path.join(MODULE_PATH, submodule)
        submodule_repo = get_repo(submodule)
        clone_url = submodule_repo.clone_url.replace(
            'https://', f'https://{GH_USERNAME}:{GH_PAT}@')

        if os.path.exists(submodule_dir):
            os.chdir(submodule_dir)
            subprocess.run(['git', 'fetch', 'origin'], check=True)
            subprocess.run(['git', 'checkout', load_branch], check=True)
            subprocess.run(['git', 'pull', 'origin', load_branch], check=True)
            os.chdir(MODULE_PATH)
        else:
            subprocess.run(['git', 'clone', '-b', load_branch,
                           clone_url, submodule], check=True)

        print(f"Updated {submodule}")
        os.chdir(ROOT_PATH)
    for submodule in SUBMODULES:
        submodule_dir = os.path.join(MODULE_FOLDER, submodule)
        subprocess.run(['git', 'add', submodule_dir], check=True)

    subprocess.run(
        ['git', 'commit', '-m', f"Update submodules to latest dev"], check=True)
    subprocess.run(['git', 'push', 'origin', current_branch], check=True)

    conversation_thread = load_initial_context()
    write_file("avatar/context/conversation_thread.txt", conversation_thread)
    print(f"{current_branch} synced to {load_branch} across repos")


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

    current_branch = get_current_branch(ROOT_PATH)

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

            print(f"Changes committed in {repo_name} on {current_branch}")
        except subprocess.CalledProcessError as e:
            print(f"Error in {repo_name}: {e}")

    os.chdir(ROOT_PATH)


def avatar_push_git(project_branch):
    print(project_branch)
    print(f"changes pushed in {repo_name} on branch {branch_name}")
