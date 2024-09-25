# greatsun-dev

Welcome to the research and development container of the credex ecosystem. Within the container of this repository are tools for running development, admin, and research modes for the credex-core API, the vimbiso-pay client, and additional clients that will we'll soon be working on, such as a web app for customer service agents and an economic modelling tool.

This container is managed by an AI "avatar" interface called greatsun-dev. The avatar *is* the development environment. It is launched in your terminal to enable you to communicate through our avatar scripts with large language model (LLM) artificial intelligences.

We are currently connecting to Anthropic's latest version of Claude 3.5 Sonnet, which has impressive "agentic" coding abilities. But the avatar script is not tied to a single LLM. In fact, the intention is to eventually integrate several models and send queries wherever is appropriate, or even to more than one LLM to compare responses. We will also be able to use this integrated LLM interface in apps we build, giving our members, clients, and customers direct access to this approach within their own context, for tasks beyond coding.

GitHub repositories and other data can be synced into the greatsun-dev container as submodules. Within the container, the avatar script gives the LLM iterative access to code bases, files, and directories to read, write, etc. As a developer working in the greatsun-dev environment, your role is to express intent to the avatar, check the code it delivers and operations it executes, make manual edits or request changes, confirm commits, and test functionality.

Your interface with the greatsun-dev avatar is at the heart of our CI/CD pipeline. With the avatar scripts opening a trilateral channel of communication and action between yourself, the artificial intelligence, and our code base, you will be able to rapidly deliver high quality code into our review, testing and deployment process.

## Implementing Your Intention
You express your intention, and the LLM uses the avatar to carry it out. Claude and the other LLMs we will use have potent and rapidly increasing capacities to handle high level abstractions and multi-step logic. When we share a purpose at a high level, the AI can assist at that level. The assistance provided is not limited to working with single lines of code, functions, or files. You can describe entire feature branches to the avatar, rapidly generate detailed work plans, and use those plans to advance the avatar through complex, multi step tasks quickly and efficiently.

To excel as a member of the greatsun-dev team:
1. stay aware of the current state, and oriented to your goal state,
2. ask good questions and probe for the most direct path,
3. use the avatar to research possibilities and help analyze options,
4. clearly state your high level plan with as many specifics as possible,
5. initiate and/or approve specific tasks,
6. review results to ensure that they move you towards your goal,
7. and test and verify because at the end of the day, you are responsible for the code you sign off on.

Every dev in this space is a project manager.

### Developer Intent #1: Current Project
The avatar automatically prepares context for the LLM. As a developer, you have two places to express your intent into this context. The first place is in the [Current Project](avatar/project/current_project.md) file. When you first enter the greatsun-dev environment, instead of grabbing a task off the current project, create your own at the bottom:
```
# But First Must Do
Get a 30 minute guided tour of greatsun-dev and the credex-ecosystem software.
```

#### Getting Started
To configure your environment, see [Configuration](docs/greatsun-dev_configuration.md). Then either:
  1. open a Codespace on `dev` or on the main branch of the project you are working on, or
  2. clone the repository locally, then
  3. launch the avatar:

  - `avatar up`: activates the avatar scripts and creates and checks out a new branch if you are on a primary branch.
    - The avatar treats branches named 'dev' or ending in '-project' as primary branches. If you are on a primary branch when you call `avatar up`, the branch for your work will be forked from that primary, and off you go.

  - `avatar load`: pulls all submodules from a remote branch to your local/codespace.
    - you need to `avatar load` on a new branch from dev to load the submodules for the first time, and you can use it to pull the latest from dev or a project branch. (test for behaviour vis-a-vis local changes. does it overwrite stashed changes?)

### Developer Intent #2: Message From Developer
The second place to express your intent is in the Message From Developer. You will initiate the conversation with the first instruction you give, and you can continue a back and forth with the LLM through the avatar. There are two ways you can communicate through the avatar. After `avatar up`, then:
  1. Enter simple queries or instructions in the terminal, and/or
  2. Enter more complex queries or instructions at the bottom of the [conversation_thread](avatar/conversation_thread.txt) file, under Message From Developer.

Press enter in the terminal.

Whatever is in the terminal will be appended to whatever is in the conversation thread and sent to the LLM. Take a look through [conversation_thread](avatar/conversation_thread.txt) to see the full conversation that you are in with the avatar, including file contents sent back and forth. A sanitized version is printed to the terminal with the file contents removed for better human readibility. (this broke, needs to be fixed. currently no terminal printing.)

### Stepping Towards Your Goal
You can use `avatar refresh` any time to restart the conversation with the context of the repo and project reassembled from the current files. You then add your intention for this specific conversation with the avatar and LLM into the Developer Instructions as above, and then work with the tool to deliver code.

The LLM can get confused if the conversation thread gets too long, if there are repetitive tweaks on the same bug going back and forth, or if multiple topics or priorities enter the thread.

Steps towards your goal are measured by the cadence of this one-conversation-at-a-time model. It's the developer's job to ensure that these iterations drive progress at a strategic level. The difference between the [Current Project](avatar/project/current_project.md) and Message From Developer is that the project will remain largly the same with small changes every time you `avatar refresh`, whereas the content of the messages back and for will leave the active memory of the avatar. Those messages are saved in conversation_thread in your commit, to be overwritten with the next commit but preserved in the repository history of greatsun-dev.

#### Independent Mini Steps
An unexpected but repeatedly established behaviour of the avatar is that when it has simple questions or wants a simple confirmation from you, it will respond to itself on your behalf. Within its response it will literally print the heading indicating your response, put words in your mouth confirming approving some minor decision it was asking about, and then proceeding with the recommendd action as if you had actually approved it.

Let's keep an eye on this behaviour, but so far the avatar usually knows to stop for important questions or when it reaches the end of its task. But this behaviour increases the chances of the script running off down a track that you do not actually intend. Always check the code before you stage and commit it.

### Entering Your First Developer Instruction
Enter something like this in the terminal or conversation thread:
```
let's get started on my guided tour. recommend a plan to complete it in 30 minutes.
```
Review the results, make any edits you see fit, or clarify your instructions and try again. Or move to the next step, like:
```
save that to the current project file
```
Chances are that's already been done on the avatar's initiative. But if not, you can request it.

## Source Control Panel
You can always stage your current state before you query the avatar, so that you can track against the changes in source control. Then when you have the changes staged for your next step forward:

  - `avatar commit`: Commits and pushes current code to all affected repos with a unified branch name and commit message.

You've now got a workplan for the next 30 minutes stored in Current Project, so `avatar refresh` both to clear the conversation and to refresh the project description being sent. With a fresh and up-to-date context, you can use the workplan in [Current Project](avatar/project/current_project.md) to move forward towards your intent. The avatar can easily reference it and step through it with commands like:
```
execute the next step in the current project
```

When the avatar pauses to await your response or next instructions, you can continue the conversation with another Developer Instruction in the terminal and/or at the bottom of the [conversation_thread](/workspaces/greatsun-dev/avatar/conversation_thread.txt), or you can use any of the 'avatar' commands.

## Branches and Commits
The avatar unifies and links your commits across all repositories, including this one. Get started on a new project by pulling the latest from 'dev' to your local or launching a codespace off 'dev' from GitHub, or launch on an existing project branch. Once your development container is live, `avatar up` for a new branch to be created for you if you are on one of these primary banches. If you launch from a branch other than 'dev' or a branch ending in '-project', your launch branch will be maintained into the avatar.

Don't hesitate to commit regularly. Multiple untested commits that move you towards your objective are expected, with testing more likely to be done on a series of commits than on each one. Staging changes can also be very helpful. You want to be able to lock in every step, and if too many changes build up you can lose it all if a wobble develops in the LLM's capacity and it makes a crazy write. Don't save your progress where it is subject to the whims of the avatar, save it in a trail of granular commits. You want to be able to refresh the context any time without significant loss of progress.

### Commit conversation_thread.txt with every commit
In order to track progress and performance of AI models, and provide insight into effective and productive query patterns, please commit your automatically updated conversation_thread.txt file with every commit.

### Two Tricks
1. If you are in the middle of a productive thread and something goes wrong, you can delete content out of the conversation_thread and restart from whatever point you want.
2. The handy undo:
 - `avatar stepback` undoes your last commit, bringing it back into staged changes whenever you need a do-over. Can be done repetitively to step way back if necessary. *(to be built)*

## Running services
All imported modules are brought online in dev mode with:
  - `avatar engage`: fires up the submodule servers.

## Intent Achieved
Once you have acheived your intent and tested your code for a feature, fix, or task:

  - `avatar submit`: Option `<project>` pushes your branches to remote, and requests a merge into a -project branch, creating it if it doesn't exist. *(buggy, do not use yet)*

Projects will consist of one or more merges from a team member's branches, with each commit possibly linked to other commits across greatsun-dev and/or the submodules. When the project (feature, fix, or refactor) is ready, it will be merged to dev, one repository at a time using GitHub web.

Once you've submitted your branch, take a new branch of the project or off dev if your project is finished, and continue your work towards the next goal.

  - **On codespaces:** close the window and create a new codespace on greatsun-dev, dev branch or your project branch.
  - **On local:** switch branches on greatsun-dev with `git checkout <dev or project-branch>`. *(to test)*

Run `avatar up` then `avatar load` for dev or your project branch, then `avatar refresh` and you are ready to go.

  - `avatar down` exits back to the terminal.

## List of Commands
Everything listed above in one place for reference:
  - `avatar up`: activates the script and creates and checks out a new branch if you are on dev.
  - `avatar refresh`: reloads the conversation from current files.
  - `avatar load`: pulls all submodules from a remote branch to your local/codespace.
  - `avatar engage`: fires up the submodule servers.
  - `avatar commit`: Commits and pushes current code to all affected repos with a unified commit message.
  - `avatar stepback` undoes your last commit, bringing it back into staged changes whenever you need a do-over. Can be done repetitively to step way back if necessary. *(to be built)*
  - `avatar submit`: Option `<project>` pushes your branches to remote, and requests a merge into a -project branch, creating it if it doesn't exist. *(buggy, do not use yet)*
  - `avatar down` exits the shell.

## Project Structure
The greatsun-dev repository consists of the following top level directories:

### /avatar
Processing iterative call/response queries to LLMs and implementing the LLM's instructions for developer approval.

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