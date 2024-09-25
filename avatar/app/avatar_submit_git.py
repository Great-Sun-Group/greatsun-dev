import os
import subprocess
from github import GithubException

from config import ROOT_REPO, SUBMODULES, ROOT_PATH, MODULE_PATH, GH_USERNAME
from basics import get_current_branch, get_repo

def avatar_submit_git(project_branch):
    if (project_branch == "dev" or project_branch == "stage" or project_branch == "prod"):
        print("not authorized")
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
                pr_title = f"{current_branch} by @{GH_USERNAME}"
                pr_body = f"Add auto-summary here based on diff for {
                    current_branch} --> {project_branch}"
                gh_repo.create_pull(
                    title=pr_title, body=pr_body, head=current_branch, base=project_branch)
                print(f"{current_branch} submitted to {
                      project_branch} in {repo_name}")
            except GithubException as e:
                print(f"Error creating pull request in {repo_name}: {e}")

    os.chdir(ROOT_PATH)
