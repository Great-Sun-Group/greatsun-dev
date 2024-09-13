#!/bin/bash

# Check if GH_PAT is set
if [ -z "$GH_PAT" ]; then
  echo "Error: GH_PAT environment variable is not set. Please set it to your GitHub Personal Access Token."
  exit 1
fi

# Function to add submodule
add_submodule() {
  local repo_url="https://$GH_PAT@github.com/Credex/$1.git"
  git submodule add $repo_url
  if [ $? -ne 0 ]; then
    echo "Error: Failed to add submodule $1"
    exit 1
  fi
}

# Add submodules
add_submodule "credex-core"
add_submodule "credex-bot"

echo "Submodules added successfully!"