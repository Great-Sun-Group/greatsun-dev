import os
import subprocess
import random
import string
import requests

# GitHub configuration
GH_USERNAME = os.environ.get('GH_USERNAME')
GH_PAT = os.environ.get('GH_PAT')
MODULE_FOLDER = 'credex-ecosystem'
SUBMODULES = [
    'credex-core',
    'vimbiso-pay'
]


def run_command(command):
    return subprocess.run(command, shell=True, check=True, capture_output=True, text=True)


def get_current_branch():
    return run_command("git rev-parse --abbrev-ref HEAD").stdout.strip()


def create_random_branch():
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=10))


def get_off_dev_branch():
    current_branch = get_current_branch()
    if current_branch == 'dev':
        new_branch = create_random_branch()
        run_command(f"git checkout -b {new_branch}")
        print(f"Branch: {new_branch}")
    else:
        print(f"Branch: {current_branch}")


def add_submodule(submodule):
    submodule_url = f"https://{GH_USERNAME}:{
        GH_PAT}@github.com/Great-Sun-Group/{submodule}"
    submodule_path = f"{MODULE_FOLDER}/{submodule}"
    run_command(f"git submodule add {submodule_url} {submodule_path}")


def update_submodule(submodule):
    submodule_path = f"{MODULE_FOLDER}/{submodule}"
    os.chdir(submodule_path)
    run_command("git fetch origin")
    run_command("git checkout dev")
    run_command("git pull origin dev")


def avatar_load_dev_git():
    get_off_dev_branch()
    current_branch = get_current_branch()

    for submodule in SUBMODULES:
        submodule_path = f"{MODULE_FOLDER}/{submodule}"
        if not os.path.exists(submodule_path):
            add_submodule(submodule)
        else:
            update_submodule(submodule)

        os.chdir(submodule_path)
        run_command(f"git checkout {
                    current_branch} 2>/dev/null || git checkout -b {current_branch}")
        os.chdir('..')

    print(f"Submodules loaded from dev and checked out to branch: {current_branch}")
    print("`avatar up` to refresh with any new context")


def has_changes(repo_path):
    os.chdir(repo_path)
    status = run_command("git status --porcelain").stdout
    os.chdir('..')
    return bool(status.strip())


def avatar_commit_git():
    current_branch = get_current_branch()
    commit_message = input("Enter commit message: ")
    commit_hashes = []

    for repo in [MODULE_FOLDER] + SUBMODULES:
        repo_path = f"/{MODULE_FOLDER}/{repo}"
        if has_changes(repo_path):
            os.chdir(repo_path)
            run_command("git add .")
            commit_output = run_command(f"git commit -m '{commit_message}'")
            commit_hash = commit_output.stdout.split()[1]
            run_command(f"git push origin {current_branch}")
            commit_hashes.append((repo, commit_hash))
            os.chdir('..')

    if commit_hashes:
        print("Commits pushed to remote branches:")
        for repo, commit_hash in commit_hashes:
            print(f"{repo}: {commit_hash}")
    else:
        print("No changes to commit.")


def create_pull_request(repo, branch, title, body):
    url = f"https://api.github.com/repos/Great-Sun-Group/{repo}/pulls"
    headers = {
        "Authorization": f"token {GH_PAT}",
        "Accept": "application/vnd.github.v3+json"
    }
    data = {
        "title": title,
        "body": body,
        "head": branch,
        "base": "dev"
    }
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 201:
        return response.json()["html_url"]
    else:
        print(f"Failed to create PR for {repo}: {response.text}")
        return None


def avatar_submit_git():
    current_branch = get_current_branch()
    if current_branch == 'dev':
        print("Cannot submit PRs from dev branch.")
        return

    title = input("Enter PR title: ")
    body = input("Enter PR description: ")

    pr_urls = []

    for repo in [MODULE_FOLDER] + SUBMODULES:
        repo_path = f"/{MODULE_FOLDER}/{repo}"
        os.chdir(repo_path)

        # Check if there are any commits to push
        if run_command(f"git log origin/dev..{current_branch}").stdout.strip():
            # Push any remaining changes
            run_command(f"git push origin {current_branch}")

            # Create pull request
            pr_url = create_pull_request(repo, current_branch, title, body)
            if pr_url:
                pr_urls.append((repo, pr_url))

        os.chdir('..')

    if pr_urls:
        print("Pull requests created:")
        for repo, url in pr_urls:
            print(f"{repo}: {url}")

        # Update PR descriptions with cross-references
        for repo, url in pr_urls:
            updated_body = body + "\n\nRelated PRs:\n" + \
                "\n".join([f"- [{r}]({u})" for r, u in pr_urls if r != repo])
            update_pr_url = url.replace(
                "github.com", "api.github.com/repos") + "?access_token=" + GH_PAT
            requests.patch(update_pr_url, json={"body": updated_body})

        print("Pull request descriptions updated with cross-references.")
    else:
        print("No changes to submit in any repository.")
