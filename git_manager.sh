#!/bin/bash

# Function to execute git commands in a repository
execute_git_command() {
    local repo=$1
    local command=$2
    echo "Executing in $repo: $command"
    if [ "$repo" = "credex-dev" ]; then
        eval "$command"
    else
        (cd "$repo" && eval "$command")
    fi
}

# Function to check if a repository has changes
has_changes() {
    local repo=$1
    if [ "$repo" = "credex-dev" ]; then
        git status --porcelain | grep -q .
    else
        (cd "$repo" && git status --porcelain | grep -q .)
    fi
}

# Repositories
repos=("credex-bot" "credex-core" "credex-dev")

# Prompt for branch name
read -p "Enter branch name: " branch_name

# Apply branch across all repositories
for repo in "${repos[@]}"; do
    execute_git_command "$repo" "git fetch --all"
    execute_git_command "$repo" "git checkout -b $branch_name origin/$branch_name || git checkout -b $branch_name"
done

# Function to create new branches
create_branches() {
    read -p "Enter new branch name: " new_branch
    for repo in "${repos[@]}"; do
        execute_git_command "$repo" "git checkout -b $new_branch"
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
            execute_git_command "$repo" "git push origin $branch_name"
        else
            echo "No changes in $repo"
        fi
    done
}

# Main menu
while true; do
    echo "1. Create new branches"
    echo "2. Checkout branches"
    echo "3. Push changes"
    echo "4. Exit"
    read -p "Choose an option: " choice
    case $choice in
        1) create_branches ;;
        2) checkout_branches ;;
        3) push_changes ;;
        4) exit 0 ;;
        *) echo "Invalid option" ;;
    esac
done