import os
import random
import string
import base64
from github import Github
from coolname import generate_slug

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


def create_random_branch():
    return generate_slug(4)


def get_repo(repo_name):
    return g.get_repo(f"Great-Sun-Group/{repo_name}")


def get_current_branch(repo):
    if isinstance(repo, str):
        repo = get_repo(repo)
    try:
        return repo.get_branch(repo.default_branch).name
    except:
        return 'dev'  # Default to 'main' if we can't determine the default branch


def get_off_dev_branch(repo):
    if isinstance(repo, str):
        repo = get_repo(repo)
    current_branch = get_current_branch(repo)
    if current_branch == 'dev':
        new_branch = create_random_branch()
        repo.create_git_ref(
            f"refs/heads/{new_branch}", repo.get_branch("dev").commit.sha)
        print(f"Created and switched to branch {new_branch}")
        return new_branch
    else:
        print(f"On branch {current_branch}")
        return current_branch


def avatar_load_dev_git():
    main_repo = get_repo(".")
    current_branch = get_off_dev_branch(main_repo)

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

    print(f"Submodules loaded from dev and checked out to branch: {
          current_branch}")
    print("`avatar up` to refresh with any new context")


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