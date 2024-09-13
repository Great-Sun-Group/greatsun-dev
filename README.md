# Credex-Dev

Development environment for the Credex ecosystem, including credex-core API and credex-bot client apps.

## Overview

This repository contains a unified development environment for the Credex ecosystem, including both credex-core and credex-bot as submodules. It provides tools for testing, data analysis, and transaction simulation.

## Prerequisites

- GitHub account with access to Credex repositories
- Git
- Docker and Docker Compose (for local development)
- Visual Studio Code (recommended)

## Setup

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

3. Build and start the development container:
   ```
   docker-compose up -d --build
   ```

4. Attach VS Code to the running container or use `docker exec` to access the container's shell.

## Usage

### Starting Services

To start all services (credex-core, credex-bot, and credex-dev), run:

```bash
bash /workspaces/credex-dev/start-services.sh
```

This will start all services and display their logs.

### Running Tests

To run automated tests:

```bash
python -m pytest tests/
```

### Analyzing Data

Data analysis functionality can be accessed through the `CredexDev` class in `main.py`. Refer to the class methods for specific analysis capabilities.

### Simulating Transactions

Transaction simulation is also available through the `CredexDev` class in `main.py`.

## Project Structure

- `credex-core/`: Submodule containing the Credex Core API
- `credex-bot/`: Submodule containing the Credex Bot
- `.devcontainer/`: Configuration files for the development container
- `tests/`: Automated tests for the development environment
- `main.py`: Main Python script for credex-dev functionality
- `requirements.txt`: Python dependencies for credex-dev
- `init-environment.sh`: Script to set up the submodules and environment
- `start-services.sh`: Script to start all services

## Contributing

Please refer to the individual submodule repositories for contribution guidelines specific to credex-core and credex-bot.

For changes to the development environment itself, please create a pull request in this repository.

## Troubleshooting

If you encounter any issues during setup or usage, please check the following:

1. Ensure all required environment variables are set correctly.
2. Check the logs of individual services in case of startup failures.
3. Verify that your GitHub Personal Access Token has the necessary permissions.
4. If you encounter issues with the Python virtual environment, try rebuilding the container or manually creating the venv:
   ```
   python3 -m venv /home/vscode/venv
   source /home/vscode/venv/bin/activate
   pip install -r requirements.txt
   ```

For more detailed troubleshooting, refer to the documentation in each submodule.

## Support

If you need assistance or have any questions, please open an issue in this repository or contact the Credex development team.
