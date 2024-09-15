# greatsun-dev README

Welcome to the research and development container of the credex ecosystem. Within the container of this repository are tools for running development mode for the credex-core API and the vimbiso-pay client (which is currently called credex-bot in the code).

This container is managed by an AI avatar called greatsun-dev, which includes logs of developer conversations with the underlying AI models that power our development. As a developer in this environment, your commits are logged, and so are the conversations with AI models that co-create those commits. As a developer, your job is to express your intent to LLMs, test and verify that the results embody your intent, and submit pull requests when you feel the code is ready to share. With a call response dialogue with LLMs you can produce high quality code at an incredibly rapid rate, and this process is the heart of both our CI/CD pipeline and our econony-modelling engine.

## Project

## /avatar
Processing queries to LLMs and their results for developer approval and implementation. Instructions and management files, as well as logs.

## central-logs
Folder to be created for compiling and monitoring logs from projects in credex-ecosystem.

## /credex-ecosystem
The credex-core API and any clients that need to be tested, developed, or employed in research. These repositories are imported directly into this dev environment, and we make commits together across all impacted repos, including this one.

- Currenty under development are:
  - credex-core, our core API on an express.js server.
  - vimbiso-pay (credex-bot), a whatsapp chatbot written in python.

## /data-analysis
Tools to analyze existing data in the credex-ecosystem

## /simulations
Folder to be created for deploying simulations consisting of patterns of transactions over time for development and research purposes.

## /tests
Folder to be created for unit tests, performance tests, etc

## Prerequisites

- GitHub account with access to Great Sun Group repositories
- Git (for local development)
- Docker and Docker Compose (for local development)
- Visual Studio Code (for local development)

## Environment Variables and Secrets

The following secrets are required for the greatsun-dev environment. These should be set in the Codespace secrets or in a `.env` file in the root directory when running locally:

- CLAUDE (optional)
  - To get this secret from Anthropic:
    1. Sign up for an account at https://www.anthropic.com or log in if you already have one.
    2. Navigate to the API section in your account settings.
    3. Generate a new API key.
    4. Copy the API key and provide it to the Claude Dev plugin.

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

## Setup

### For Codespaces

1. Set up GitHub Secrets:
   - Go to your personal GitHub Settings->Codespaces and Add New Secret for each, giving it access to the credex-dev repository.

2. Create a new Codespace:
   - Go to the main page of the credex-dev repository
   - Click on the "Code" button
   - Select the "Codespaces" tab
   - Click "Create codespace on main"

3. The Codespace will automatically set up the environment and submodules using the `init-environment.sh` script.

### For Local Development (this needs to be tested)

1. Clone this repository:
   ```
   git clone https://github.com/Credex/credex-dev.git
   cd credex-dev
   ```

2. Create a `.env` file in the root of the project based on .env.example

3. Build and start the development container:
   ```
   docker-compose up -d --build
   ```

4. Attach VS Code to the running container or use `docker exec` to access the container's shell.

