import os
import subprocess
import sys
import time
import uuid
from dotenv import load_dotenv

load_dotenv()

# Configuration
CONFIG = {
    "greatsun_dev_dir": "/workspaces/greatsun-dev",
    "credex_ecosystem_dir": "/workspaces/greatsun-dev/credex-ecosystem",
    "modules": [
        {
            "name": "credex-core",
            "repo_url": "https://github.com/Great-Sun-Group/credex-core.git",
            "branch": "dev",
            "install_command": "npm install",
            "start_command": "npm run dev",
            "requirements_file": None
        },
        {
            "name": "vimbiso-pay",
            "repo_url": "https://github.com/Great-Sun-Group/vimbiso-pay.git",
            "branch": "dev",
            "install_command": "pip install -r requirements.txt",
            "start_command": "python app/manage.py runserver 0.0.0.0:8000",
            "requirements_file": "requirements.txt"
        }
    ]
}

def run_command(command, cwd=None):
    """Run a shell command and return its output."""
    try:
        result = subprocess.run(command, shell=True, check=True, text=True, capture_output=True, cwd=cwd)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Error executing command: {command}")
        print(f"Error message: {e.stderr}")
        return None

def check_dev_manager_secrets():
    """Check if dev-manager secrets are set in the environment."""
    required_secrets = ["CLAUDE", "GH_USERNAME", "GH_PAT"]
    missing_secrets = [secret for secret in required_secrets if not os.getenv(secret)]
    
    if missing_secrets:
        print("Error: The following required secrets are missing for dev-manager:")
        for secret in missing_secrets:
            print(f"- {secret}")
        return False
    return True

def initialize_environment():
    """Initialize the greatsun-dev environment."""
    print("Initializing greatsun-dev environment...")

    if not check_dev_manager_secrets():
        return False

    # Clone or update modules
    for module in CONFIG["modules"]:
        module_path = os.path.join(CONFIG["credex_ecosystem_dir"], module["name"])
        if not os.path.exists(module_path):
            print(f"Cloning {module['name']}...")
            run_command(f"git clone {module['repo_url']} {module_path}")
        else:
            print(f"Updating {module['name']}...")
            run_command(f"git fetch origin {module['branch']}", cwd=module_path)
            run_command(f"git checkout {module['branch']}", cwd=module_path)
            run_command(f"git pull origin {module['branch']}", cwd=module_path)

        # Install dependencies
        print(f"Installing dependencies for {module['name']}...")
        run_command(module["install_command"], cwd=module_path)

    # Create central-logs directory
    os.makedirs(os.path.join(CONFIG["greatsun_dev_dir"], "central-logs"), exist_ok=True)

    print("Environment initialization complete!")
    return True

def execute_git_command(module_name, command):
    """Execute a git command in the specified module."""
    module_path = os.path.join(CONFIG["credex_ecosystem_dir"], module_name)
    return run_command(command, cwd=module_path)

def has_changes(module_name):
    """Check if a module has changes."""
    return execute_git_command(module_name, "git status --porcelain") != ""

def create_branches(new_branch=None):
    """Create new branches in all modules."""
    if not new_branch:
        new_branch = f"feature-{time.strftime('%Y%m%d-%H%M%S')}"
    
    for module in CONFIG["modules"]:
        execute_git_command(module["name"], "git fetch --all")
        execute_git_command(module["name"], f"git checkout -b {new_branch} origin/{module['branch']} || git checkout -b {new_branch}")

def checkout_branches(branch_name):
    """Checkout branches in all modules."""
    for module in CONFIG["modules"]:
        execute_git_command(module["name"], f"git checkout {branch_name}")

def push_changes(commit_message):
    """Push changes in all modules."""
    commit_uuid = str(uuid.uuid4())
    for module in CONFIG["modules"]:
        if has_changes(module["name"]):
            execute_git_command(module["name"], "git add .")
            execute_git_command(module["name"], f'git commit -m "{commit_message} [{commit_uuid}]"')
            execute_git_command(module["name"], "git push origin $(git rev-parse --abbrev-ref HEAD)")
        else:
            print(f"No changes in {module['name']}")

def start_service(module):
    """Start a service and log its output."""
    log_file = os.path.join(CONFIG["greatsun_dev_dir"], "central-logs", f"{module['name']}.log")
    module_path = os.path.join(CONFIG["credex_ecosystem_dir"], module["name"])
    
    if os.path.isdir(module_path):
        print(f"Starting {module['name']}...")
        run_command(f"{module['start_command']} > {log_file} 2>&1 &", cwd=module_path)
    else:
        print(f"Warning: {module['name']} directory not found. Skipping.")

def start_all_services():
    """Start all services."""
    for module in CONFIG["modules"]:
        start_service(module)

    # Wait for services to start
    timeout = 60
    start_time = time.time()
    while True:
        all_started = True
        for module in CONFIG["modules"]:
            log_file = os.path.join(CONFIG["greatsun_dev_dir"], "central-logs", f"{module['name']}.log")
            if not os.path.exists(log_file) or "Starting development server" not in run_command(f"cat {log_file}"):
                all_started = False
                break

        if all_started:
            print("All services started successfully!")
            break

        if time.time() - start_time >= timeout:
            print(f"Timeout: One or more services failed to start within {timeout} seconds.")
            print(f"Check the log files in {CONFIG['greatsun_dev_dir']}/central-logs/ for more information.")
            return False

        time.sleep(1)

    return True

def stop_all_services():
    """Stop all services."""
    print("Stopping all services...")
    for module in CONFIG["modules"]:
        run_command(f"pkill -f '{module['start_command']}'")
    print("All services stopped.")

def view_logs(log_choice):
    """View logs for the selected service(s)."""
    log_files = {str(i+1): f"{module['name']}.log" for i, module in enumerate(CONFIG["modules"])}
    log_files[str(len(CONFIG["modules"]) + 1)] = [f"{module['name']}.log" for module in CONFIG["modules"]]

    if log_choice in log_files:
        if isinstance(log_files[log_choice], list):
            for log_file in log_files[log_choice]:
                print(f"--- {log_file} ---")
                print(run_command(f"tail -n 50 central-logs/{log_file}", cwd=CONFIG["greatsun_dev_dir"]))
                print("\n")
        else:
            print(run_command(f"tail -n 50 central-logs/{log_files[log_choice]}", cwd=CONFIG["greatsun_dev_dir"]))
    else:
        print("Invalid choice")

def main():
    """Main function to handle deployment operations."""
    if len(sys.argv) < 2:
        print("Usage: python module_deployment.py [init|create_branches|checkout|push|start|stop|logs]")
        sys.exit(1)

    action = sys.argv[1]

    if action == "init":
        initialize_environment()
    elif action == "create_branches":
        new_branch = sys.argv[2] if len(sys.argv) > 2 else None
        create_branches(new_branch)
    elif action == "checkout":
        if len(sys.argv) < 3:
            print("Please provide a branch name to checkout.")
            sys.exit(1)
        checkout_branches(sys.argv[2])
    elif action == "push":
        if len(sys.argv) < 3:
            print("Please provide a commit message.")
            sys.exit(1)
        push_changes(" ".join(sys.argv[2:]))
    elif action == "start":
        start_all_services()
    elif action == "stop":
        stop_all_services()
    elif action == "logs":
        if len(sys.argv) < 3:
            print(f"Please provide a log choice (1-{len(CONFIG['modules']) + 1}).")
            sys.exit(1)
        view_logs(sys.argv[2])
    else:
        print("Invalid action. Choose 'init', 'create_branches', 'checkout', 'push', 'start', 'stop', or 'logs'.")

if __name__ == "__main__":
    main()