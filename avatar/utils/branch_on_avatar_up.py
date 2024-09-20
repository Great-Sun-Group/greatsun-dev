import os
import random
import string
import subprocess


def get_current_branch(repo_path):
    try:
        result = subprocess.run(['git', 'rev-parse', '--abbrev-ref', 'HEAD'],
                                cwd=repo_path,
                                capture_output=True,
                                text=True,
                                check=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError:
        return None


def create_random_branch(repo_path):
    # Generate a random branch name
    random_string = ''.join(random.choices(
        string.ascii_lowercase + string.digits, k=8))
    new_branch_name = f"feature-{random_string}"

    try:
        # Create and checkout the new branch
        subprocess.run(['git', 'checkout', '-b', new_branch_name],
                       cwd=repo_path,
                       check=True)
        print(f"Created and checked out new branch: {new_branch_name}")
        return new_branch_name
    except subprocess.CalledProcessError:
        print("Failed to create and checkout new branch")
        return None


def main():
    repo_path = os.path.join(os.getcwd(), "greatsun-dev")

    if not os.path.exists(repo_path):
        print("greatsun-dev repository not found in the current directory")
        return

    current_branch = get_current_branch(repo_path)

    if current_branch is None:
        print("Failed to get current branch")
        return

    print(f"Current branch: {current_branch}")

    if current_branch == "dev":
        new_branch = create_random_branch(repo_path)
        if new_branch:
            print(f"Switched to new branch: {new_branch}")
    else:
        print("Not on 'dev' branch. No new branch created.")

    # Your existing command line interface code goes here
    # ...


if __name__ == "__main__":
    main()
