# greatsun-dev README

Welcome to the research and development container of the credex ecosystem. Within the container of this repository are tools for running development mode for the credex-core API and the vimbiso-pay client (which is currently called credex-bot in the code).

This container is managed by an AI avatar called greatsun-dev. The avatar *is* the development environment. It has access to:
  - the full scope of multiple underlying LLMs,
  - our current codebases and commit histories,
  - and the logged conversations that members of the dev team have had with the LLMs.

As a developer in this environment, your job is to express your intent to LLMs, do quality control and verify that the results embody your intent, and submit pull requests when you feel the code is ready to go to the next step of review. Your commits are logged granularly, and so are the conversations with AI models that co-create those commits. With a call/response dialogue with LLMs, you can produce high quality code at an incredibly rapid rate, and this process is the heart of the CI/CD pipeline of the credex ecosystemand, and also at the heart of our engine for econonic modeling.

An LLM is an underlying model, to which every query is a fresh query. This means every query needs to include full context. When you query the LLMs underneath greatsun-dev, we assemble a context and response instructions for the LLM, including your message and optionally a linked file. If the LLM wants to request more context, it informs the codebase, which resends the entire original query, with the requested files attached.

When the LLM responds with recommended code changes, it's response is parsed and it's recommendations executed as a proposed commit. Review the commit and see if it moves you in the direction that you want to go. Query again if you want changes, or make smal edits manually if that's most efficient.

### Commits
As a developer on the Great Sun dev team, you use commits to closely monitor the actions of the avatar and ensure it is proceeding towards your intent. The avatar will overwrite files when you query it, so every commit becomes a reference point for checking the next steps. Commit often, so that every query to the LLM can be checked against a prior commit without an overwhelming number of changes accumulating.

Commits are done in a commonly named and identified commit across all affected repos with the `command here` command to the avatar.

#### Undo
If since the last commit you've made changes that you don't want to lose, and the avatar messes with your code, the undo command works on each file changed to undo the last changes made by the avatar.

### Command line interface
You will communicate with the avatar through a terminal. Responses are logged and recommended actions are saved imediately to files.
- `avatar up` launches the avatar.

#### LLM commands
1. To send a query to the LLM, which is currently hardcoded to only Claude 3.5 Sonnet, update [avatar/messageToSend.md](avatar/messageToSend.md) with your message and press Enter in the terminal.
2. To send a query from messageToSend (can be empty) and the contents of a first reference file to the LLM, enter the path of the file in the terminal and press Enter.

#### Shell commands
Specific commands to the avatar will not go to an LLM, but will be processed in-context by code within greatsun-dev. These commands are:
- `git manage`: stages, commits, and pushes current code to all repos with a unified commit message description (to be built)

Exit
- `down` exits the avatar back to the shell.

## Project
Our project consists of the following top level directories:

## /avatar
Processing queries to LLMs and their results for developer approval and implementation. LLM instructions and management files, as well as logs.

## /central-logs
Folder to be created for compiling and monitoring logs from projects in credex-ecosystem.

## /credex-ecosystem
The credex-core API and any clients that need to be tested, developed, or employed in research. These repositories are imported directly into this dev environment, and we make commits together across all impacted repos, including this one.

- Currenty under development are:
  - credex-core, our core API on an express.js server.
  - vimbiso-pay (credex-bot), a whatsapp chatbot written in python.

## /data-analysis
Folder to be created for tools to analyze existing data in the credex-ecosystem

## /docs
Documentation for the greatsun-dev environment.

## /simulations
Folder to be created for deploying simulations consisting of patterns of transactions over time for development and research purposes.

## /tests
Folder to be created for unit tests, performance tests, etc

# Getting started
If you've already set your configuration, just type `avatar up` in the terminal to get started

# Developer resources
- To configure your environment, see [Configuration](docs/greatsun-dev_configuration.md)