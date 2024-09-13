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

## Environment Variables and Secrets

The following secrets are required for the Credex development environment. These should be set in the Codespace secrets or in a `.env` file in the root directory when running locally:

- CLAUDE
  - To get this secret from Anthropic:
    1. Sign up for an account at https://www.anthropic.com or log in if you already have one.
    2. Navigate to the API section in your account settings.
    3. Generate a new API key.
    4. Copy the API key and use it as the value for CLAUDE.

- DJANGO_SECRET
  - create your own unique random string
- GH_PAT
  - To get this secret from GitHub:
    1. Log in to your GitHub account.
    2. Go to Settings > Developer settings > Personal access tokens.
    3. Click "Generate new token" and select the necessary scopes (repo, workflow, read:org should be sufficient).
    4. Copy the generated token and use it as the value for GH_PAT.

- JWT_SECRET
  - create your own unique random string
- NEO_4J_LEDGER_SPACE_BOLT_URL
- NEO_4J_LEDGER_SPACE_PASS
- NEO_4J_LEDGER_SPACE_USER
- NEO_4J_SEARCH_SPACE_BOLT_URL
- NEO_4J_SEARCH_SPACE_PASS
- NEO_4J_SEARCH_SPACE_USER
  - To set up Neo4j Aura databases:
    1. Go to https://neo4j.com/cloud/aura/ and sign up for two separate accounts using different email addresses.
    2. For each account, create a new database instance. One should be name ledgerSpace and the other searchSpace.
    3. Once the databases are created, you'll be provided with connection details.
    4. Use the Bolt URL, username, and password for each database to fill in the corresponding environment variables.
    5. The LEDGER_SPACE variables correspond to one database, and the SEARCH_SPACE variables to the other.

- OPEN_EXCHANGE_RATES_API
  - To get this secret from Open Exchange Rates:
    1. Go to https://openexchangerates.org/ and sign up for an account.
    2. Once logged in, navigate to your account dashboard.
    3. Look for your App ID or API Key.
    4. Copy this key and use it as the value for OPEN_EXCHANGE_RATES_API.

- WHATSAPP_BOT_API_KEY
  - create your own unique random string

Refer to the `.env.example` file in the root directory for a template of these environment variables. Remember to never commit your actual `.env` file with real values to version control.

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
