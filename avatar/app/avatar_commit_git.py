import os
import uuid
import subprocess
from pathlib import Path

from config import MODULE_PATH, ROOT_PATH, SUBMODULES, ROOT_REPO
from basics import get_current_branch

def avatar_commit_git():
    commit_message = input("Enter commit message: ")
    commit_id = str(uuid.uuid4())
    full_commit_message = f"{commit_message}\n\nCommit-ID: {commit_id}"

    repos = [ROOT_REPO] + SUBMODULES
    current_branch = get_current_branch()

    for repo_name in repos:
        repo_path = ROOT_PATH if repo_name == ROOT_REPO else os.path.join(
            MODULE_PATH, repo_name)
        os.chdir(repo_path)

        # Save a simple file in each repo
        greatsun_devtracker = f"{current_branch}\n\n{full_commit_message}"
        file_path = Path("greatsun-dev_tracker.txt")
        with open(file_path, 'w') as f:
            f.write(greatsun_devtracker)

        # Stage the file
        subprocess.run(['git', 'add', str(file_path)], check=True)

        # Check if the branch exists, create it if it doesn't
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
            subprocess.run(['git', 'checkout', current_branch], check=True)
            print(f"Switched to existing branch {
                  current_branch} in {repo_name}")

        # Commit the changes
        try:
            subprocess.run(
                ['git', 'commit', '-m', full_commit_message], check=True)
            print(f"Changes committed locally in {
                  repo_name} on {current_branch}")
        except subprocess.CalledProcessError as e:
            print(f"Error in {repo_name}: {e}")

    os.chdir(ROOT_PATH)
