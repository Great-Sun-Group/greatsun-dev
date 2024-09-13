#!/bin/bash

# Function to add submodule
add_submodule() {
  local repo_url="https://${GH_PAT:-$GITHUB_TOKEN}@github.com/Credex/$1.git"
  git submodule add $repo_url
  if [ $? -ne 0 ]; then
    echo "Error: Failed to add submodule $1"
    exit 1
  fi
}

# Check if running in Codespaces
if [ -n "$CODESPACES" ]; then
  echo "Running in Codespaces environment"
  # Use GitHub Secrets
  if [ -z "$GITHUB_TOKEN" ]; then
    echo "Error: GITHUB_TOKEN is not set. Please set it in your GitHub Secrets."
    exit 1
  fi
else
  echo "Running in local environment"
  # Use .env file
  if [ -f .env ]; then
    export $(cat .env | xargs)
  else
    echo "Error: .env file not found. Please create one with your GitHub Personal Access Token (GH_PAT)."
    exit 1
  fi

  if [ -z "$GH_PAT" ]; then
    echo "Error: GH_PAT is not set in .env file. Please set it to your GitHub Personal Access Token."
    exit 1
  fi
fi

# Add submodules
add_submodule "credex-core"
add_submodule "credex-bot"

echo "Submodules added successfully!"

# Install dependencies and set up the environment
cd /workspaces/credex-dev/credex-core && npm install
cd /workspaces/credex-dev/credex-bot && pip install -r requirements.txt

# Install dependencies for credex-dev
cd /workspaces/credex-dev
pip install -r requirements.txt

echo "Environment setup complete!"