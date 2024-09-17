#!/bin/bash

# greatsun-dev-manager.sh
# This script combines Git management and service control for the greatsun-dev environment

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
CREDEX_CORE_DIR="/workspaces/greatsun-dev/credex-core"
VIMBISO_PAY_DIR="/workspaces/greatsun-dev/vimbiso-pay"
fi
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
execute_git_command "$repo" "git checkout -b $new_branch origin/$new_branch || git checkout -b $new_branch"
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
echo "1. Git Operations"
echo "2. Start Services"
echo "3. Stop Services"
echo "4. View Logs"
echo "5. Exit"
read -p "Choose an option: " choice

case $choice in
1)
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
2) start_all_services ;;
3) stop_all_services ;;
4) view_logs ;;
5) exit 0 ;;
*) echo "Invalid option" ;;
esac
done
}

# Check if script is run on startup
if [ "$1" = "startup" ]; then
echo "Running on startup. Creating a new branch and starting services."
load_config
create_branches "feature-$(date +%Y%m%d-%H%M%S)"
start_all_services
else
load_config
main_menu
fi

Now, let's create a configuration file to store repository paths and other settings:


{
"repositories": ["vimbiso-pay", "credex-core", "greatsun-dev"],
"greatsun_dev_dir": "/workspaces/greatsun-dev",
"credex_core_dir": "/workspaces/greatsun-dev/credex-core",
"vimbiso_pay_dir": "/workspaces/greatsun-dev/vimbiso-pay"
}
