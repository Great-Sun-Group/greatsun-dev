# greatsun-dev README

Welcome to the research and development container of the credex ecosystem. Within the container of this repository are tools for running development mode for the credex-core API and the vimbiso-pay client (which is currently called credex-bot in the code).

This container is managed by an AI avatar called greatsun-dev. This avatar includes the full scope of multiple underlying LLMs, our current codebases and commit histories, and the logged conversations that members of the dev team have had with the LLMs. As a developer in this environment, your commits are logged granularly, and so are the conversations with AI models that co-create those commits. As a developer, your job is to express your intent to LLMs, do quality control and verify that the results embody your intent, and submit pull requests when you feel the code is ready to go to the next step of review. With a call/response dialogue with LLMs, you can produce high quality code at an incredibly rapid rate, and this process is the heart of both our CI/CD pipeline and our econony-modelling engine.

An LLM is an underlying model, to which every query is a fresh query. This means every query needs to include full context. When you query greatsun-dev, we assemble a context and response instructions, including your message and optionally a linked file. If the LLM wants to request more context, it informs the codebase, which resends the entire original query, with the requested files attached.

When the LLM responds, it's response is parsed and it's recommendations executed as a proposed commit. Review the commit and see if it moves you in the direction that you want to go. Query again if you want changes, or make smal edits manually if that's most efficient.

### Commits
As a human developer on the Great Sun dev team, you use commits to closely monitor the actions of the avatar and ensure it is proceeding towards your intent. The avatar will overwrite files, so every commit becomes a reference point for checking the next steps. Commit often, so that every query to the LLM can be checked against a prior commit without an overwhelming number of changes accumulating.

Commits are done in a commonly named and identified commit across all affected repos with the `command here` command to the avatar.

#### Undo
If since the last commit you've made changes that you don't want to lose, and the avatar messes with your code, the undo command works on each file changed.

### Command line interface
You will communicate with the avatar through a terminal. Responses are logged and recommended actions are saved imediately to files.
- `avatar up` launches the avatar.

#### LLM commands
1. To send a query to the LLM, which is currently hardcoded to only Claude 3.5 Sonnet, update [avatar/messageToSend.md](avatar/messageToSend.md) with your message and press Enter in the terminal.
2. To send a query (can be empty) and the contents of a first reference file to the LLM, enter the path of the file in the terminal and press Enter.

#### Shell commands
Specific commands to the avatar will not go to an LLM, but will be processed in-context by code within greatsun-dev. These commands are:
- `command`: description
- `command`: description

Exit
- `down` exits the avatar back to the shell.

## Project
Our project consists of the following top level directories:

## /avatar
Processing queries to LLMs and their results for developer approval and implementation. Instructions and management files, as well as logs.

## /central-logs
Folder to be created for compiling and monitoring logs from projects in credex-ecosystem.

## /credex-ecosystem
The credex-core API and any clients that need to be tested, developed, or employed in research. These repositories are imported directly into this dev environment, and we make commits together across all impacted repos, including this one.

- Currenty under development are:
  - credex-core, our core API on an express.js server.
  - vimbiso-pay (credex-bot), a whatsapp chatbot written in python.

## /data-analysis
Folder to be created for tools to analyze existing data in the credex-ecosystem

## /simulations
Folder to be created for deploying simulations consisting of patterns of transactions over time for development and research purposes.

## /tests
Folder to be created for unit tests, performance tests, etc

## Prerequisites

- GitHub account with access to Great Sun Group repositories
### For local development
- Git
- Docker and Docker Compose
- Visual Studio Code

## Environment Variables and Secrets

The following secrets are required for the greatsun-dev environment. These should be set in the Codespace secrets or in a `.env` file in the root directory when running locally:

- CLAUDE
  Get this secret from Anthropic or your admin.
  - From Anthropic:
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
This will technically give the avatar that you connect with access to all your github repos. Don't import any into this development container. Instead we'll make this environment duplicable to work on other projects and provide them with their own avatar.

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
   - Go to your personal GitHub Settings->Codespaces and Add New Secret for each, giving it access to the greatsun-dev repository.

2. Create a new Codespace:
   - Go to the main page of the greatsun-dev repository
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

