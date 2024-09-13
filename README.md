# credex-dev
Development environment for the credex-core API and client apps

## Unified Development Environment Setup

This repository contains a unified development environment for the Credex ecosystem, including both credex-core and credex-bot as submodules, with credex-dev implemented in Python for testing, data analysis, and transaction simulation.

### For Codespaces

1. Set up GitHub Secrets:
   - Go to your GitHub repository settings
   - Navigate to Secrets and variables > Codespaces
   - Add a new repository secret named `GH_PAT` with your GitHub Personal Access Token

2. Create a new Codespace:
   - Go to the main page of this repository
   - Click on the "Code" button
   - Select the "Codespaces" tab
   - Click "Create codespace on main"

3. The Codespace will automatically set up the environment and submodules using the `init-environment.sh` script.

### For Local Development

1. Clone this repository:
   ```
   git clone https://github.com/Credex/credex-dev.git
   cd credex-dev
   ```

2. Create a `.env` file in the root of the project with your GitHub Personal Access Token:
   ```
   GH_PAT=your_personal_access_token
   ```

3. Open the project in Visual Studio Code and reopen in a devcontainer when prompted, or run:
   ```
   code .
   ```

4. The devcontainer will automatically set up the environment and submodules using the `init-environment.sh` script.

## Starting the Services

To start all services (credex-core, credex-bot, and credex-dev), run:

```bash
bash /workspaces/credex-dev/start-services.sh
```

This will start credex-core, credex-bot, and credex-dev services and display their logs.

## Repository Structure

- `credex-core/`: Submodule containing the Credex Core API (Express.js)
- `credex-bot/`: Submodule containing the Credex Bot (Python)
- `.devcontainer/`: Configuration files for the development container
- `init-environment.sh`: Script to securely set up the submodules and environment
- `start-services.sh`: Script to start all services
- `main.py`: Main Python script for credex-dev
- `requirements.txt`: Python dependencies for credex-dev

## Contributing

Please refer to the individual submodule repositories for contribution guidelines specific to credex-core and credex-bot.

For changes to the development environment itself, please create a pull request in this repository.

## Development in credex-dev

The `main.py` file in the root directory contains the main logic for credex-dev. It includes functionality for running automated tests, analyzing data, and simulating transactions. To extend or modify this functionality:

1. Edit the `main.py` file to add or change features.
2. If you need to add new Python dependencies, add them to the `requirements.txt` file.
3. Run `pip install -r requirements.txt` to install any new dependencies.
4. Use the `start-services.sh` script to run your updated credex-dev along with credex-core and credex-bot.

Remember to test your changes thoroughly and ensure they don't interfere with the functioning of credex-core or credex-bot.
