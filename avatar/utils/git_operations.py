import os
import subprocess
from github import Github
from coolname import generate_slug
from utils.file_operations import load_initial_context, write_file

# GitHub configuration
GH_USERNAME = os.environ.get('GH_USERNAME')
GH_PAT = os.environ.get('GH_PAT')
MODULE_FOLDER = 'credex-ecosystem'
SUBMODULES = [
    'credex-core',
    'vimbiso-pay'
]

# Initialize Github client
g = Github(GH_PAT)


def get_repo(repo_name):
    return g.get_repo(f"Great-Sun-Group/{repo_name}")


def get_current_branch(repo=None):
    if repo is None:
        # Get the current branch name using Git command
        try:
            current_branch = subprocess.check_output(['git', 'rev-parse', '--abbrev-ref', 'HEAD'],
                                                     stderr=subprocess.DEVNULL).decode().strip()
            return current_branch
        except subprocess.CalledProcessError:
            print("Failed to get current branch. Are you in a Git repository?")
            return None
    else:
        if isinstance(repo, str):
            repo = get_repo(repo)
        try:
            return repo.get_branch(repo.default_branch).name
        except:
            return 'dev'  # Default to 'dev' if we can't determine the default branch


def get_off_dev_branch():
    current_branch = get_current_branch()
    if current_branch == 'dev':
        new_slug = generate_slug(2)
        new_branch = f"avatar-of-{new_slug}"

        # Create and checkout new branch
        try:
            subprocess.run(['git', 'checkout', '-b', new_branch],
                           check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            print(f"on branch {new_branch}")
        except subprocess.CalledProcessError:
            print(f"Failed to create and switch to new branch: {new_branch}")
            return current_branch

        # Update the branch in the GitHub repo
        repo = get_repo('greatsun-dev')
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
    main_repo = get_repo('greatsun-dev')
    current_branch = get_current_branch()
    if current_branch == 'dev':
        print("you are currently on the dev branch")
        return

    for submodule in SUBMODULES:
        submodule_repo = get_repo(submodule)
        submodule_branch = current_branch

        # Update submodule reference in main repo
        try:
            submodule_content = main_repo.get_contents(
                f"{MODULE_FOLDER}/{submodule}")
            main_repo.update_file(
                submodule_content.path,
                f"Update {submodule} submodule",
                submodule_repo.get_branch(submodule_branch).commit.sha,
                submodule_content.sha,
                branch=current_branch
            )
        except:
            main_repo.create_file(
                f"{MODULE_FOLDER}/{submodule}",
                f"Add {submodule} submodule",
                submodule_repo.get_branch(submodule_branch).commit.sha,
                branch=current_branch
            )

    conversation_thread = load_initial_context()
    write_file("avatar/context/conversation_thread.txt",
            conversation_thread)
    print(f"{current_branch} reloaded")


def has_changes(repo, branch):
    if isinstance(repo, str):
        repo = get_repo(repo)
    # Compare the branch with its base (usually 'dev')
    comparison = repo.compare('dev', branch)
    return len(comparison.files) > 0


def avatar_commit_git():
    commit_message = input("Enter commit message: ")
    commit_hashes = []
    changes_found = False

    repos = [MODULE_FOLDER] + SUBMODULES

    for repo_name in repos:
        try:
            repo = get_repo(repo_name)
            branch = get_current_branch(repo)
            if has_changes(repo, branch):
                changes_found = True
                # Create a new commit
                ref = repo.get_git_ref(f"heads/{branch}")
                tree = repo.get_git_tree(ref.object.sha)
                new_commit = repo.create_git_commit(
                    commit_message, tree, [ref.object])
                ref.edit(new_commit.sha)
                commit_hashes.append((repo_name, new_commit.sha))
                print(f"Commit pushed to {repo_name}: {new_commit.sha}")
            else:
                print(f"No changes detected in {repo_name}")
        except Exception as e:
            print(f"Error processing repository {repo_name}: {str(e)}")

    if commit_hashes:
        print("\nCommits pushed to remote branches:")
        for repo, commit_hash in commit_hashes:
            print(f"{repo}: {commit_hash}")
    elif changes_found:
        print("Changes were found, but commits failed. Check the error messages above.")
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
    main_repo = get_repo(MODULE_FOLDER)
    current_branch = get_current_branch(main_repo)
    if current_branch == 'dev':
        print("Cannot submit PRs from dev branch.")
        return

    title = input("Enter PR title: ")
    body = input("Enter PR description: ")

    pr_urls = []

    repos = [MODULE_FOLDER] + SUBMODULES

    for repo_name in repos:
        repo = get_repo(repo_name)
        if has_changes(repo, current_branch):
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
