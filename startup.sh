#!/bin/bash

# Make sure the avatar script is executable
chmod +x /workspaces/greatsun-dev/avatar/avatar

# Add alias to .bashrc
echo 'alias avatar="python3 /workspaces/greatsun-dev/avatar/avatar"' >> ~/.bashrc

# Source .bashrc to make the alias available immediately
source ~/.bashrc

# Print a message
echo "Avatar environment is ready. You can now use the 'avatar' command."