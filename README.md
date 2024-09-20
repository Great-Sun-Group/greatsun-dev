# greatsun-dev

Welcome to the research and development container of the credex ecosystem. Within the container of this repository are tools for running development, admin, and research modes for the credex-core API, the vimbiso-pay client, and additional clients that will we'll soon be working on, such as a web interface for customer service agents and an economic modelling tool.

This container is managed by an AI "avatar" interface called greatsun-dev. The avatar *is* the development environment, launched in your terminal to communicate through our avatar scripts with large language model (LLM) artificial intelligences.

We are currently connected to Anthropic's latest version of Claude 3.5 Sonnet, which has impressive "agentic" coding abilities. But the avatar script is not tied to a single LLM. In fact, the intention is to eventually integrate several models and send queries wherever is appropriate, or even to more than one LLM to compare responses. We will also be able to use this integrated LLM interface in the apps we are building, giving our members, clients, and customers direct access to this approach within their own context.

The avatar script gives the LLM iterative access to the project code bases to read, write, etc. As a developer working in the greatsun-dev environment, your role is to express intent to the avatar, check the code it delivers, make manual edits or request changes, confirm commits, and test functionality.

With the avatar scripts providing an interface between you, the artificial intelligence, and the code base, you are able to rapidly deliver high quality code into our review, testing and deployment process. Your interface with the greatsun-dev avatar is at the heart of our CI/CD pipeline.

## Implementing Your Intention
You express your intention, and the LLM uses the avatar to carry it out. Claude and the other LLMs we will use have potent and rapidly increasing capacities to handle higher level abstractions and multi-step logic. When we share a purpose at a high level, it can assist at that level. It is not limited to instructions to create specific lines of code, functions, or even full files. You can describe entire feature branches and use the generated workplans to step through complex, multi step tasks quickly and efficiently.

A developer will succeed in this container by being able to clearly and specifically communicate high level intent, direct research, analyze options, approve specific tasks, and review results. Every dev here is a project manager. Even if you don't know the language being used, the avatar will orient you as you go if you ask the right questions, and you'll soon be up to speed.

### Developer Intent #1: Current Project
The avatar automatically prepares context for the LLM. As a developer, you have two places to express your intent into this context. The first place is in the [Current Project](avatar/context/current_project.md) file. Clear the contents and put a couple of sentences here about what you are trying to accomplish over the coming hours or days. When you first enter the greatsun-dev environment, try a current project like:
```
# Current Project

Orient myself to the greatsun-dev environment and the credex-ecosystem submodules. Understand the most important features and functions of all repos, and how they are linked together by greatsun-dev.
```

#### Getting Started
To configure your environment, see [Configuration](docs/greatsun-dev_configuration.md). Then with a Codespace opened on `dev` or the repository cloned locally, launch the avatar.
  - `avatar up`: installs anthropic dependency if not found, and creates and checks out a new branch if you are on dev, generates the avatar context.
  - `avatar load`: installs the submodules set in [Configuration](docs/greatsun-dev_configuration.md) into the credex-ecosystem. Creates and checks out branches matching your current branch name in greatsun-dev.
 - `avatar reset`: Reloads the context, including the readme files from the submodules.

### Developer Intent #2: Developer Instructions
The second place to express your intent is in the Developer Instructions. There are two places you can do this. First launch with `avatar up`, then:
  1. Enter simple queries or instructions in the terminal, and/or
  2. Enter more complex queries or instructions that require formatting or editing at the bottom of the [conversation_thread](avatar/context/conversation_thread.txt) file, under Initial Developer Instructions or Developer Response.

Press enter in the terminal. Whatever is in the terminal will be appended to the conversation thread and sent to the LLM. Take a look through [conversation_thread](avatar/context/conversation_thread.txt) to see what is being sent to the LLM.

### Stepping Towards Your Goal
When you launch `avatar up`, the current context of the repo and project is assembled. You then add your overall intention for this specific exchange with the avatar and LLM into the Developer Instructions as above. The LLM will get confused if the conversation_thread gets too long, so the Initial Developer Intention should be something that can be acheived within the context of a single exchange. Experience will guide this, and models will continue to improve.

Larger projects are handled piece by piece and tracked in the [Current Project](avatar/context/current_project.md) file. To get started, use a Developer Instruction like:
```
review avatar/context/current_project.md and append a full workplan
```
Review the results, stage, commit, and `avatar reset` to reload the context including the updated Current Project file.

Now use the workplan in [Current Project](avatar/context/current_project.md) to move forward towards your intent. The avatar can easily reference it and step through it with commands like:
```
execute step 2 in the current project and mark it complete
```

When the avatar pauses to await your response or next instructions, you can continue the conversation with another Developer Instruction in the terminal and/or at the bottom of the [conversation_thread](/workspaces/greatsun-dev/avatar/context/conversation_thread.txt).

## Branches and Commits
The avatar unifies and links your commits across all repositories, including this one. If you launch the avatar from the dev branch, a new branch will be created for you. If you launch from another branch, that branch will be maintained into the avatar. On launch, branches of the same name as your branch in greatsun-dev will be created (if necessary) and checked out in all the submodule repos.

- `avatar commit`: Stages, commits, and pushes current code to all repos with a unified commit message.

Stage and/or commit before every avatar command. The avatar may behave unpredictably and make destructive changes. If changes that appear to be solid from the prior query are staged or committed, new changes can be reviewed and easily discarded without losing anything else. Multiple untested commits that move you towards your objective are expected, with testing more likely to be done on a series of commits than on each one.

## Intent Achieved
Once you have acheived your intent and tested your code to satsifaction for a feature or a fix:
  - `avatar submit`: Creates a pull request for the current branch into the dev branch across all repositories.

Merges into dev will be tested in greatsun-dev for quality assurance, but the merges themselves will be approved in each individual repository. The branches and any codespaces still on it will be deleted after the merge is approved, so do not continue to work on a branch after the merge has been submitted

Continue your work with a new branch off dev.
  - `avatar down` exits back to the terminal.

**On codespaces:** close the window and create a new codespace on dev.
**On local:** switch branches on greatsun-dev with `git checkout dev` and pull the latest with `git pull origin dev` then relaunch with `avatar up`.

## All Commands
Everything listed above in one place for reference:
  - `avatar up`: installs anthropic dependency if not found, and creates and checks out a new branch if you are on dev.
  - `avatar load`: installs the submodules set in [Configuration](docs/greatsun-dev_configuration.md) into the credex-ecosystem, creating and checking out branches matching your current branch name in greatsun-dev.
  - `avatar reset`: Reloads the context, including the updated Current Project file.
  - `avatar commit`: Stages, commits, and pushes current code to all repos with a unified commit message.
  - `avatar submit`: Creates a pull request for the current branch into the dev branch across all repositories.
  - `avatar down` exits back to the terminal.

## Project Structure
Our project consists of the following top level directories:

### /avatar
Processing queries to LLMs and their results for developer approval and implementation. LLM instructions and context, management files, and conversation logs.

### /central-logs
Folder to be created for compiling and monitoring logs from the projects in credex-ecosystem and from greatsun-dev.

### /credex-ecosystem
The credex-core API and any clients that need to be tested, developed, or employed in research. These repositories are imported directly into this dev environment, and we make commits together across all impacted repos, including this one.

- Currently under development are:
  - credex-core: our core API on an express.js server.
  - vimbiso-pay: a WhatsApp chatbot written in Python.

### /data-analysis
Folder to be created for tools to analyze existing data in the credex-ecosystem.

### /docs
Documentation for the greatsun-dev environment.

### /simulations
Folder to be created for deploying simulations consisting of patterns of transactions over time for development and research purposes.

### /tests
Folder to be created for unit tests, performance tests, etc.