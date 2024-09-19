#!/bin/bash

# greatsun-dev-manager.sh
# This script combines Git management, service control, and environment initialization for the greatsun-dev environment

set -e

# Configuration
CONFIG_FILE="/workspaces/greatsun-dev/greatsun-dev-config.json"

# Load configuration
load_config() {
    if [ -f "$CONFIG_FILE" ]; then
        mapfile -t repos < <(jq -r '.repositories[]' "$CONFIG_FILE")
        GREATSUN_DEV_DIR=$(jq -r '.greatsun_dev_dir' "$CONFIG_FILE")
        CREDEX_CORE_DIR=$(jq -r '.credex_core_dir' "$CONFIG_FILE")
        VIMBISO_PAY_DIR=$(jq -r '.vimbiso_pay_dir' "$CONFIG_FILE")
    else
        echo "Configuration file not found. Using default values."
        repos=("vimbiso-pay" "credex-core" "greatsun-dev")
        GREATSUN_DEV_DIR="/workspaces/greatsun-dev"
        CREDEX_CORE_DIR="/workspaces/greatsun-dev/credex-ecosystem/credex-core"
        VIMBISO_PAY_DIR="/workspaces/greatsun-dev/credex-ecosystem/vimbiso-pay"
    fi
}

# Function to check if a secret is set
check_secret() {
    if [ -z "${!1}" ]; then
        echo "Error: $1 is not set. Please set it in your environment or .env file."
        return 1
    fi
    return 0
}

# Function to initialize the environment
initialize_environment() {
    echo "Initializing greatsun-dev environment..."

    # Check if running in Codespaces
    if [ -n "$CODESPACES" ]; then
        echo "Running in Codespaces environment"
        # Use GitHub Secrets
        if [ -z "$GITHUB_TOKEN" ]; then
            echo "Error: GITHUB_TOKEN is not set. Please set it in your GitHub Secrets."
            return 1
        fi
    else
        echo "Running in local environment"
        # Use .env file
        if [ -f .env ]; then
            export $(cat .env | xargs)
        else
            echo "Error: .env file not found. Please create one."
            return 1
        fi
    fi

    # Check for required secrets
    local required_secrets=(
        "CLAUDE" "DJANGO_SECRET" "GH_USERNAME" "GH_PAT" "JWT_SECRET"
        "NEO_4J_LEDGER_SPACE_BOLT_URL" "NEO_4J_LEDGER_SPACE_PASS" "NEO_4J_LEDGER_SPACE_USER"
        "NEO_4J_SEARCH_SPACE_BOLT_URL" "NEO_4J_SEARCH_SPACE_PASS" "NEO_4J_SEARCH_SPACE_USER"
        "OPEN_EXCHANGE_RATES_API" "WHATSAPP_BOT_API_KEY"
    )

    for secret in "${required_secrets[@]}"; do
        check_secret "$secret" || return 1
    done

    # Function to add submodule
    add_submodule() {
        local repo_url="https://${GH_PAT:-$GITHUB_TOKEN}@github.com/Great-Sun-Group/$1.git"
        git submodule add $repo_url || true
        git submodule update --init --recursive
    }

    # Add submodules
    add_submodule "credex-ecosystem/credex-core"
    add_submodule "credex-ecosystem/vimbiso-pay"

    echo "Submodules added successfully!"

    # Import latest from "dev" branches
    echo "Importing latest from 'dev' branches..."
    (cd "$CREDEX_CORE_DIR" && git fetch origin dev && git checkout dev && git pull origin dev)
    (cd "$VIMBISO_PAY_DIR" && git fetch origin dev && git checkout dev && git pull origin dev)

    # Create and activate virtual environment
    python3 -m venv /home/vscode/venv
    source /home/vscode/venv/bin/activate

    # Install dependencies and set up the environment
    (cd "$CREDEX_CORE_DIR" && npm install)
    (cd "$VIMBISO_PAY_DIR" && pip install -r requirements.txt)
    (cd "$GREATSUN_DEV_DIR" && pip install -r requirements.txt)

    # Create central-logs directory
    mkdir -p "$GREATSUN_DEV_DIR/central-logs"

    echo "Environment initialization complete!"
    return 0
}

# Function to execute git commands in a repository
execute_git_command() {
    local repo=$1
    local command=$2
    echo "Executing in $repo: $command"
    if [ "$repo" = "greatsun-dev" ]; then
        (cd "$GREATSUN_DEV_DIR" && eval "$command")
    elif [ "$repo" = "credex-core" ]; then
        (cd "$CREDEX_CORE_DIR" && eval "$command")
    elif [ "$repo" = "vimbiso-pay" ]; then
        (cd "$VIMBISO_PAY_DIR" && eval "$command")
    else
        echo "Unknown repository: $repo"
    fi
}

# Function to check if a repository has changes
has_changes() {
    local repo=$1
    if [ "$repo" = "greatsun-dev" ]; then
        (cd "$GREATSUN_DEV_DIR" && git status --porcelain | grep -q .)
    elif [ "$repo" = "credex-core" ]; then
        (cd "$CREDEX_CORE_DIR" && git status --porcelain | grep -q .)
    elif [ "$repo" = "vimbiso-pay" ]; then
        (cd "$VIMBISO_PAY_DIR" && git status --porcelain | grep -q .)
    else
        echo "Unknown repository: $repo"
        return 1
    fi
}

# Function to create new branches
create_branches() {
    local new_branch=$1
    if [ -z "$new_branch" ]; then
        read -p "Enter new branch name: " new_branch
    fi
    for repo in "${repos[@]}"; do
        execute_git_command "$repo" "git fetch --all"
        execute_git_command "$repo" "git checkout -b $new_branch origin/dev || git checkout -b $new_branch"
    done
}

# Function to checkout branches
checkout_branches() {
    read -p "Enter branch name to checkout: " checkout_branch
    for repo in "${repos[@]}"; do
        execute_git_command "$repo" "git checkout $checkout_branch"
    done
}

# Function to push changes
push_changes() {
    read -p "Enter commit message: " commit_message
    uuid=$(uuidgen)
    for repo in "${repos[@]}"; do
        if has_changes "$repo"; then
            execute_git_command "$repo" "git add ."
            execute_git_command "$repo" "git commit -m \"$commit_message [$uuid]\""
            execute_git_command "$repo" "git push origin $(git rev-parse --abbrev-ref HEAD)"
        else
            echo "No changes in $repo"
        fi
    done
}

# Function to start a service
start_service() {
    local service_name=$1
    local start_command=$2
    local log_file="$GREATSUN_DEV_DIR/central-logs/${service_name}.log"

    echo "Starting ${service_name}..."
    if [ -d "$GREATSUN_DEV_DIR/${service_name}" ]; then
        cd "$GREATSUN_DEV_DIR/${service_name}"
        eval "${start_command} > ${log_file} 2>&1 &"
    else
        echo "Warning: ${service_name} directory not found. Skipping."
    fi
}

# Function to start all services
start_all_services() {
    echo "Starting greatsun-dev..."
    cd "$GREATSUN_DEV_DIR"
    python main.py > "$GREATSUN_DEV_DIR/central-logs/greatsun-dev.log" 2>&1 &

    echo "Starting credex-core..."
    start_service "credex-core" "npm run dev"

    echo "Starting vimbiso-pay..."
    cd "$VIMBISO_PAY_DIR"
    source venv/bin/activate
    start_service "vimbiso-pay" "python app/manage.py runserver 0.0.0.0:8000"
    deactivate

    cd "$GREATSUN_DEV_DIR"

    # Wait for services to start
    timeout=60
    start_time=$(date +%s)
    while true; do
        if grep -q "Starting development server" "$GREATSUN_DEV_DIR/central-logs/credex-core.log" && \
           grep -q "Starting development server at http://0.0.0.0:8000/" "$GREATSUN_DEV_DIR/central-logs/vimbiso-pay.log" && \
           grep -q "vimbiso-pay is running" "$GREATSUN_DEV_DIR/central-logs/greatsun-dev.log"; then
            echo "All services started successfully!"
            break
        fi

        current_time=$(date +%s)
        if [ $((current_time - start_time)) -ge $timeout ]; then
            echo "Timeout: One or more services failed to start within ${timeout} seconds."
            echo "Check the log files in $GREATSUN_DEV_DIR/central-logs/ for more information."
            return 1
        fi

        sleep 1
    done
}

# Function to stop all services
stop_all_services() {
    echo "Stopping all services..."
    pkill -f "python main.py"
    pkill -f "npm run dev"
    pkill -f "python app/manage.py runserver"
    echo "All services stopped."
}

# Function to view logs
view_logs() {
    echo "1. greatsun-dev log"
    echo "2. credex-core log"
    echo "3. vimbiso-pay log"
    echo "4. All logs"
    read -p "Choose a log to view (1-4): " log_choice

    case $log_choice in
        1) tail -f "$GREATSUN_DEV_DIR/central-logs/greatsun-dev.log" ;;
        2) tail -f "$GREATSUN_DEV_DIR/central-logs/credex-core.log" ;;
        3) tail -f "$GREATSUN_DEV_DIR/central-logs/vimbiso-pay.log" ;;
        4) tail -f "$GREATSUN_DEV_DIR/central-logs/greatsun-dev.log" "$GREATSUN_DEV_DIR/central-logs/credex-core.log" "$GREATSUN_DEV_DIR/central-logs/vimbiso-pay.log" ;;
        *) echo "Invalid choice" ;;
    esac
}

# Main menu
main_menu() {
    while true; do
        echo "greatsun-dev Manager"
        echo "1. Initialize Environment"
        echo "2. Git Operations"
        echo "3. Start Services"
        echo "4. Stop Services"
        echo "5. View Logs"
        echo "6. Exit"
        read -p "Choose an option: " choice

        case $choice in
            1) initialize_environment ;;
            2)
                echo "Git Operations:"
                echo "a. Create new branches"
                echo "b. Checkout branches"
                echo "c. Push changes"
                read -p "Choose a Git operation: " git_choice
                case $git_choice in
                    a) create_branches ;;
                    b) checkout_branches ;;
                    c) push_changes ;;
                    *) echo "Invalid option" ;;
                esac
                ;;
            3) start_all_services ;;
            4) stop_all_services ;;
            5) view_logs ;;
            6) exit 0 ;;
            *) echo "Invalid option" ;;
        esac
    done
}

# Check if script is run on startup
if [ "$1" = "startup" ]; then
    echo "Running on startup. Initializing environment, creating a new branch, and starting services."
    load_config
    initialize_environment || exit 1
    create_branches "feature-$(date +%Y%m%d-%H%M%S)" || true
    start_all_services || true
else
    load_config
    main_menu
fi