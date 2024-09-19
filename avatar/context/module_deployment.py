import os
import subprocess
import sys
import time
import uuid

# Configuration
CONFIG = {
    "repositories": ["vimbiso-pay", "credex-core", "greatsun-dev"],
    "greatsun_dev_dir": "/workspaces/greatsun-dev",
    "credex_core_dir": "/workspaces/greatsun-dev/credex-ecosystem/credex-core",
    "vimbiso_pay_dir": "/workspaces/greatsun-dev/credex-ecosystem/vimbiso-pay"
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

def check_secret(secret_name):
    """Check if a secret is set in the environment."""
    if secret_name not in os.environ:
        print(f"Error: {secret_name} is not set. Please set it in your environment or .env file.")
        return False
    return True

def initialize_environment():
    """Initialize the greatsun-dev environment."""
    print("Initializing greatsun-dev environment...")

    # Check if running in Codespaces
    if "CODESPACES" in os.environ:
        print("Running in Codespaces environment")
        if not check_secret("GITHUB_TOKEN"):
            return False
    else:
        print("Running in local environment")
        if os.path.exists(".env"):
            with open(".env") as f:
                for line in f:
                    key, value = line.strip().split("=", 1)
                    os.environ[key] = value
        else:
            print("Error: .env file not found. Please create one.")
            return False

    # Check for required secrets
    required_secrets = [
        "CLAUDE", "DJANGO_SECRET", "GH_USERNAME", "GH_PAT", "JWT_SECRET",
        "NEO_4J_LEDGER_SPACE_BOLT_URL", "NEO_4J_LEDGER_SPACE_PASS", "NEO_4J_LEDGER_SPACE_USER",
        "NEO_4J_SEARCH_SPACE_BOLT_URL", "NEO_4J_SEARCH_SPACE_PASS", "NEO_4J_SEARCH_SPACE_USER",
        "OPEN_EXCHANGE_RATES_API", "WHATSAPP_BOT_API_KEY"
    ]

    for secret in required_secrets:
        if not check_secret(secret):
            return False

    # Add submodules
    def add_submodule(repo):
        repo_url = f"https://{os.environ.get('GH_PAT', os.environ.get('GITHUB_TOKEN'))}@github.com/Great-Sun-Group/{repo}.git"
        run_command(f"git submodule add {repo_url} || true")
        run_command("git submodule update --init --recursive")

    add_submodule("credex-ecosystem/credex-core")
    add_submodule("credex-ecosystem/vimbiso-pay")

    print("Submodules added successfully!")

    # Import latest from "dev" branches
    print("Importing latest from 'dev' branches...")
    run_command("git fetch origin dev && git checkout dev && git pull origin dev", cwd=CONFIG["credex_core_dir"])
    run_command("git fetch origin dev && git checkout dev && git pull origin dev", cwd=CONFIG["vimbiso_pay_dir"])

    # Create and activate virtual environment
    run_command("python3 -m venv /home/vscode/venv")
    # Note: Activation should be done in the shell where the script is run

    # Install dependencies
    run_command("npm install", cwd=CONFIG["credex_core_dir"])
    run_command("pip install -r requirements.txt", cwd=CONFIG["vimbiso_pay_dir"])
    run_command("pip install -r requirements.txt", cwd=CONFIG["greatsun_dev_dir"])

    # Create central-logs directory
    os.makedirs(os.path.join(CONFIG["greatsun_dev_dir"], "central-logs"), exist_ok=True)

    print("Environment initialization complete!")
    return True

def execute_git_command(repo, command):
    """Execute a git command in the specified repository."""
    repo_dir = CONFIG.get(f"{repo}_dir", CONFIG["greatsun_dev_dir"])
    return run_command(command, cwd=repo_dir)

def has_changes(repo):
    """Check if a repository has changes."""
    return execute_git_command(repo, "git status --porcelain") != ""

def create_branches(new_branch=None):
    """Create new branches in all repositories."""
    if not new_branch:
        new_branch = f"feature-{time.strftime('%Y%m%d-%H%M%S')}"
    
    for repo in CONFIG["repositories"]:
        execute_git_command(repo, "git fetch --all")
        execute_git_command(repo, f"git checkout -b {new_branch} origin/dev || git checkout -b {new_branch}")

def checkout_branches(branch_name):
    """Checkout branches in all repositories."""
    for repo in CONFIG["repositories"]:
        execute_git_command(repo, f"git checkout {branch_name}")

def push_changes(commit_message):
    """Push changes in all repositories."""
    commit_uuid = str(uuid.uuid4())
    for repo in CONFIG["repositories"]:
        if has_changes(repo):
            execute_git_command(repo, "git add .")
            execute_git_command(repo, f'git commit -m "{commit_message} [{commit_uuid}]"')
            execute_git_command(repo, "git push origin $(git rev-parse --abbrev-ref HEAD)")
        else:
            print(f"No changes in {repo}")

def start_service(service_name, start_command):
    """Start a service and log its output."""
    log_file = os.path.join(CONFIG["greatsun_dev_dir"], "central-logs", f"{service_name}.log")
    service_dir = CONFIG.get(f"{service_name}_dir")
    
    if service_dir and os.path.isdir(service_dir):
        print(f"Starting {service_name}...")
        run_command(f"{start_command} > {log_file} 2>&1 &", cwd=service_dir)
    else:
        print(f"Warning: {service_name} directory not found. Skipping.")

def start_all_services():
    """Start all services."""
    start_service("greatsun-dev", "python main.py")
    start_service("credex-core", "npm run dev")
    start_service("vimbiso-pay", "source venv/bin/activate && python app/manage.py runserver 0.0.0.0:8000")

    # Wait for services to start
    timeout = 60
    start_time = time.time()
    while True:
        credex_core_started = "Starting development server" in run_command("cat central-logs/credex-core.log", cwd=CONFIG["greatsun_dev_dir"])
        vimbiso_pay_started = "Starting development server at http://0.0.0.0:8000/" in run_command("cat central-logs/vimbiso-pay.log", cwd=CONFIG["greatsun_dev_dir"])
        greatsun_dev_started = "vimbiso-pay is running" in run_command("cat central-logs/greatsun-dev.log", cwd=CONFIG["greatsun_dev_dir"])

        if credex_core_started and vimbiso_pay_started and greatsun_dev_started:
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
    run_command("pkill -f 'python main.py'")
    run_command("pkill -f 'npm run dev'")
    run_command("pkill -f 'python app/manage.py runserver'")
    print("All services stopped.")

def view_logs(log_choice):
    """View logs for the selected service(s)."""
    log_files = {
        "1": "greatsun-dev.log",
        "2": "credex-core.log",
        "3": "vimbiso-pay.log",
        "4": ["greatsun-dev.log", "credex-core.log", "vimbiso-pay.log"]
    }

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
            print("Please provide a log choice (1-4).")
            sys.exit(1)
        view_logs(sys.argv[2])
    else:
        print("Invalid action. Choose 'init', 'create_branches', 'checkout', 'push', 'start', 'stop', or 'logs'.")

if __name__ == "__main__":
    main()