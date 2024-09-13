# credex-dev
Development environment for the credex-core api and client apps

## Unified Development Environment Setup

This repository contains a unified development environment for the credex ecosystem, including both credex-core and credex-bot as submodules. Follow these steps to set up your development environment:

1. Clone this repository:
   ```
   git clone https://github.com/Credex/credex-dev.git
   cd credex-dev
   ```

2. Create a GitHub Personal Access Token (PAT):
   - Go to GitHub Settings > Developer settings > Personal access tokens
   - Click "Generate new token"
   - Give it a name (e.g., "Credex Dev Environment")
   - Select the necessary scopes (at least 'repo' for private repositories)
   - Copy the generated token

3. Set your PAT as an environment variable:
   ```
   export GH_PAT=your_personal_access_token
   ```

4. Open the project in Visual Studio Code and reopen in a devcontainer when prompted, or run:
   ```
   code . && code --remote-env GH_PAT=$GH_PAT .
   ```

5. The devcontainer will automatically set up the submodules using your PAT.

6. Once the setup is complete, you can start working with both credex-core and credex-bot in the same environment.

For more detailed instructions, refer to the `.envSetup.md` file in this repository.

## Repository Structure

- `credex-core/`: Submodule containing the Credex Core API
- `credex-bot/`: Submodule containing the Credex Bot
- `.devcontainer/`: Configuration files for the development container
- `setup-submodules.sh`: Script to securely set up the submodules

## Getting Started

After setting up the development environment, you can start the servers by running:

```bash
bash /workspaces/credex-dev/start-servers.sh
```

This will start both credex-core and credex-bot services.

## Contributing

Please refer to the individual submodule repositories for contribution guidelines specific to credex-core and credex-bot.

For changes to the development environment itself, please create a pull request in this repository.
