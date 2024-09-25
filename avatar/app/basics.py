import json
import os
import subprocess
from coolname import generate_slug
from github import Github
from typing import Dict, Any
from pathlib import Path
from config import BASE_DIR, GH_PAT, GH_ORGANIZATION, ROOT_REPO

g = Github(GH_PAT)


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


def load_initial_context() -> str:
    initial_context = [
        read_file(BASE_DIR / "avatar/app/avatar_orientation.md"),
        read_file(BASE_DIR / "avatar/app/response_instructions.txt"),
        f"\n\n*** README.md ***\n\n",
        read_file(BASE_DIR / "README.md"),
        f"\n\n*** credex-core/README.md ***\n\n",
        read_file(BASE_DIR / "credex-ecosystem/credex-core/README.md"),
        f"\n\n*** credex-ecosystem/vimbiso-pay/README.md ***\n\n",
        read_file(BASE_DIR / "credex-ecosystem/vimbiso-pay/README.md"),
        f"*** FULL DIRECTORY TREE ***\n\n",
        json.dumps(get_directory_tree(BASE_DIR), indent=2),
        f"\n\n*** avatar/project/current_project.md ***\n\n",
        read_file(BASE_DIR / "avatar/project/current_project.md"),
        f"\n\n*** MESSAGE FROM DEVELOPER @{
            os.environ.get('GH_USERNAME')} ***\n\n",
    ]
    return ''.join(initial_context)


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
