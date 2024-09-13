# Setting Up a New Unified Development Environment for Credex

To create a unified development environment that includes both credex-core and credex-bot, follow these steps:

1. Create a new GitHub repository (e.g., "credex-dev-env"):
   - Go to GitHub and create a new repository
   - Initialize it with a README.md

2. Clone the new repository locally:
   ```
   git clone https://github.com/your-username/credex-dev-env.git
   cd credex-dev-env
   ```

3. Create a GitHub Personal Access Token (PAT):
   - Go to GitHub Settings > Developer settings > Personal access tokens
   - Click "Generate new token"
   - Give it a name (e.g., "Credex Dev Environment")
   - Select the necessary scopes (at least 'repo' for private repositories)
   - Copy the generated token and keep it secure

4. Create a setup-submodules.sh script in the root of the repository:
   ```bash
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
   ```

5. Make the script executable:
   ```
   chmod +x setup-submodules.sh
   ```

6. Run the setup-submodules.sh script to add credex-core and credex-bot as submodules:
   ```
   GH_PAT=your_personal_access_token ./setup-submodules.sh
   ```

7. Copy the updated devcontainer.json to the new repository:
   - Create a .devcontainer directory: `mkdir .devcontainer`
   - Copy the updated devcontainer.json into this directory

8. Update the devcontainer.json file:
   - Update the "dockerComposeFile" path to point to the credex-core submodule:
     ```json
     "dockerComposeFile": "./credex-core/compose.yaml",
     ```
   - Ensure the "workspaceFolder" is set to "/workspaces"
   - Add a "postCreateCommand" to run the setup-submodules.sh script

9. Create a new start-servers.sh script in the root of the new repository:
   ```bash
   #!/bin/bash

   # Start credex-core
   echo "Starting credex-core..."
   cd /workspaces/credex-core
   npm install
   npm run dev > /workspaces/credex-core.log 2>&1 &

   # Start credex-bot
   echo "Starting credex-bot..."
   cd /workspaces/credex-bot
   pip install -r requirements.txt
   python main.py > /workspaces/credex-bot.log 2>&1 &

   # Wait for servers to start
   timeout=60
   start_time=$(date +%s)
   while true; do
       if grep -q "Server is running" "/workspaces/credex-core.log" && grep -q "Bot is running" "/workspaces/credex-bot.log"; then
           echo "Both servers started successfully!"
           break
       fi

       current_time=$(date +%s)
       if [ $((current_time - start_time)) -ge $timeout ]; then
           echo "Timeout: One or both servers failed to start within ${timeout} seconds."
           echo "credex-core log:"
           tail -n 20 /workspaces/credex-core.log
           echo "credex-bot log:"
           tail -n 20 /workspaces/credex-bot.log
           exit 1
       fi

       sleep 1
   done

   # Keep the script running and tail the log files
   tail -f /workspaces/credex-core.log /workspaces/credex-bot.log
   ```

10. Commit and push all changes to the new repository:
    ```
    git add .
    git commit -m "Initial setup for unified Credex development environment"
    git push origin main
    ```

11. Set up a new Codespace:
    - Go to the new "credex-dev-env" repository on GitHub
    - Click on the "Code" button
    - Select the "Codespaces" tab
    - Click "Create codespace on main"

12. Once the new Codespace is created, it should automatically run the setup-submodules.sh and start-servers.sh scripts. If not, run them manually:
    ```
    GH_PAT=your_personal_access_token ./setup-submodules.sh
    bash /workspaces/start-servers.sh
    ```

13. Verify that both credex-core and credex-bot are running correctly.

This new setup creates a dedicated repository for the unified development environment, correctly tracking all configuration files and scripts while including credex-core and credex-bot as submodules. This approach ensures that changes to the development environment are properly version-controlled and can be easily shared across the team. Each developer can use their own Personal Access Token to clone the private repositories securely.