import os
import shutil
import subprocess

from config import MODULE_PATH, ROOT_PATH, SUBMODULES, GH_PAT, GH_USERNAME, BASE_DIR
from basics import get_current_branch, get_repo, load_initial_context, write_file


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
