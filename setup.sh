#!/bin/bash

# Install Python dependencies
pip install -r requirements.txt

# Set up the development environment
# Create a script to set up the avatar command
cat << EOF > /usr/local/bin/setup-avatar.sh
#!/bin/bash
alias avatar="python3 /workspaces/greatsun-dev/avatar/avatar"
EOF

# Make the setup script executable
chmod +x /usr/local/bin/setup-avatar.sh

# Make sure the avatar script is executable
chmod +x /workspaces/greatsun-dev/avatar/avatar

# Add sourcing of the setup script to .bashrc if it doesn't exist
grep -qxF 'source /usr/local/bin/setup-avatar.sh' ~/.bashrc || echo 'source /usr/local/bin/setup-avatar.sh' >> ~/.bashrc

# Start the necessary services
# Start the avatar
python3 /workspaces/greatsun-dev/avatar/avatarUp.py

echo "Development environment set up and services started."