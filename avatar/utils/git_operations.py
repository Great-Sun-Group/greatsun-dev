
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
