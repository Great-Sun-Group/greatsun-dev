import os
import subprocess
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


def avatar_load_dev_git():
    current_branch = get_current_branch()
    if current_branch == 'dev':
        print("You are currently on the dev branch")
        return

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
            subprocess.run(['git', 'checkout', 'dev'], check=True)
            subprocess.run(['git', 'pull', 'origin', 'dev'], check=True)
            os.chdir(MODULE_PATH)
        else:
            subprocess.run(['git', 'clone', '-b', 'dev',
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
    print(f"{current_branch} synced to `dev` branches")


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

    repos = [ROOT_REPO] + SUBMODULES

    for repo_name in repos:
        repo_path = ROOT_PATH if repo_name == ROOT_REPO else os.path.join(
            MODULE_PATH, repo_name)

        try:
            # Change to the repository directory
            os.chdir(repo_path)

            # Check if there are staged changes
            result = subprocess.run(
                ['git', 'diff', '--staged', '--quiet'], capture_output=True)

            if result.returncode == 1:  # There are staged changes
                changes_found = True

                # Commit the changes
                subprocess.run(
                    ['git', 'commit', '-m', commit_message], check=True)

                # Push the changes
                current_branch = get_current_branch(repo_path)
                subprocess.run(
                    ['git', 'push', 'origin', current_branch], check=True)

                print(f"Changes committed and pushed in {repo_name}")
            else:
                print(f"No staged changes in {repo_name}")

        except subprocess.CalledProcessError as e:
            print(f"Error in {repo_name}: {e}")
        finally:
            # Always return to the root directory
            os.chdir(ROOT_PATH)

    if changes_found:
        print("Commits pushed to remote branches.")
    else:
        print("No changes to commit in any repository.")


def create_pull_request(repo, branch, title, body):
    try:
        pr = repo.create_pull(title=title, body=body, head=branch, base='dev')
        return pr.html_url
    except Exception as e:
        print(f"Failed to create PR for {repo.name}: {str(e)}")
        return None


def avatar_submit_git():
    current_branch = get_current_branch(ROOT_PATH)
    if current_branch == 'dev':
        print("Cannot submit PRs from dev branch.")
        return

    title = input("Enter PR title: ")
    body = input("Enter PR description: ")

    pr_urls = []

    repos = [ROOT_REPO] + SUBMODULES

    for repo_name in repos:
        repo = get_repo(repo_name)
        repo_path = ROOT_PATH if repo_name == ROOT_REPO else os.path.join(
            MODULE_PATH, repo_name)
        if has_staged_changes(repo_path):
            pr_url = create_pull_request(repo, current_branch, title, body)
            if pr_url:
                pr_urls.append((repo_name, pr_url))

    if pr_urls:
        print("Pull requests created:")
        for repo, url in pr_urls:
            print(f"{repo}: {url}")

        # Update PR descriptions with cross-references
        for repo_name, url in pr_urls:
            repo = get_repo(repo_name)
            pr_number = int(url.split('/')[-1])
            pr = repo.get_pull(pr_number)
            updated_body = body + "\n\nRelated PRs:\n" + \
                "\n".join([f"- [{r}]({u})" for r,
                          u in pr_urls if r != repo_name])
            pr.edit(body=updated_body)

        print("Pull request descriptions updated with cross-references.")
    else:
        print("No changes to submit in any repository.")
