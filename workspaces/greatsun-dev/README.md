[Content starts on the next line]
# greatsun-dev README

Welcome to the research and development container of the credex ecosystem. Within this repository are tools for running development mode for the credex-core API and the vimbiso-pay client.

This container is managed by an AI avatar called greatsun-dev. The avatar *is* the development environment. It has access to:
  - the full scope of multiple underlying LLMs,
  - our current codebases and commit histories,
  - and the logged conversations that members of the dev team have had with the LLMs.

As a developer in this environment, your job is to express your intent to LLMs, do quality control and verify that the results embody your intent, and submit pull requests when you feel the code is ready for the next step of review. Your commits are logged granularly, along with the conversations with AI models that co-create those commits. With a call/response dialogue with LLMs, you can produce high-quality code at an incredibly rapid rate. This process is at the heart of the CI/CD pipeline of the credex ecosystem and our engine for economic modeling.

An LLM is an underlying model, to which every query is a fresh query. This means every query needs to include full context. When you query the LLMs underneath greatsun-dev, we assemble a context and response instructions for the LLM, including your message and optionally a linked file. If the LLM wants to request more context, it informs the codebase, which resends the entire original query with the requested files attached.

When the LLM responds with recommended code changes, its response is parsed and its recommendations are executed as a proposed commit. Review the commit and see if it moves you in the direction you want to go. Query again if you want changes, or make small edits manually if that's most efficient.

## Environment Management

Use the `greatsun-dev-manager.sh` script to manage the environment:

```
./greatsun-dev-manager.sh {init|start|stop|status}
```

- `init`: Initialize the environment (create directories, clone submodules)
- `start`: Start the greatsun-dev avatar
- `stop`: Stop the greatsun-dev avatar
- `status`: Check the status of the greatsun-dev avatar

## Avatar Interaction

Once the avatar is started, you will communicate with it through a terminal.

### LLM Commands
1. To send a query to the LLM (currently Claude 3.5 Sonnet), update `avatar/messageFromDeveloper.md` with your message and press Enter in the terminal.
2. To send a query from messageFromDeveloper.md (can be empty) and the contents of a reference file to the LLM, enter the path of the file in the terminal and press Enter.

### Shell Commands
Specific commands to the avatar will not go to an LLM but will be processed by code within greatsun-dev:
- `avatar commit`: stages, commits, and pushes current code to all repos with a unified commit message description, and clears the avatar context.
- `avatar clear`: clears the avatar context.
- `avatar down`: exits the avatar back to the shell.

## Project Structure

- `/avatar`: Processing queries to LLMs and their results for developer approval and implementation.
- `/central-logs`: Compiling and monitoring logs from the projects in credex-ecosystem and from greatsun-dev.
- `/credex-ecosystem`: Submodules for credex-core API and vimbiso-pay client.
- `/data-analysis`: Tools to analyze existing data in the credex-ecosystem.
- `/docs`: Documentation for the greatsun-dev environment.
- `/simulations`: Deploying simulations of transaction patterns for development and research.
- `/tests`: Unit tests, performance tests, etc.

## Getting Started

1. Initialize the environment: `./greatsun-dev-manager.sh init`
2. Start the avatar: `./greatsun-dev-manager.sh start`
3. Interact with the avatar as described in the "Avatar Interaction" section.

## Developer Resources

- For environment configuration, see [Configuration](docs/greatsun-dev_configuration.md)