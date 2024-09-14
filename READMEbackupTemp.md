## Usage

### Starting Services and Managing Git

To start all services (credex-core, credex-bot, and credex-dev) and manage Git operations across all repositories, follow these steps:

1. Start the services:
   ```bash
   bash /workspaces/credex-dev/start-services.sh
   ```
   This will start all services and display their logs.

2. For Git management, use `git_manager.sh` to help manage Git operations across all three repositories (credex-bot, credex-core, and credex-dev) simultaneously:

   a. Make the script executable (if not already):
      ```bash
      chmod +x /workspaces/credex-dev/git_manager.sh
      ```

   b. Run the script:
      ```bash
      ./git_manager.sh
      ```

   c. The script will prompt you to enter a branch name. This branch will be created or checked out in all three repositories.

   d. After that, you'll see a menu with the following options:
      - Create new branches
      - Checkout branches
      - Push changes
      - Exit

   e. When pushing changes, you'll be prompted for a commit message. The script will automatically generate a UUID and append it to your commit message. It will then stage, commit, and push changes in all repositories that have modifications.

This script streamlines the process of managing branches and commits across the Credex ecosystem, ensuring consistency across all repositories.

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
- `git_manager.sh`: Script to manage Git operations across all repositories

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
