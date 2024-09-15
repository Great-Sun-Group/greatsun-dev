import os

API_KEY = os.getenv("CLAUDE")
if not API_KEY:
    raise ValueError("CLAUDE API key not found in environment variables")

LOGS_DIRECTORY = "avatar/context/conversationLog"
RESPONSE_INSTRUCTIONS = "avatar/context/responseInstructions.md"
AVATAR_README = "avatarREADME.md"
README = "README.md"
MESSAGE_TO_SEND = "avatar/messageToSend.md"
CONTEXT_DIR = "avatar/context"
TERMINAL_COMMANDS_FILE = "avatar/terminalCommands.txt"
CURRENT_RESPONSE_FILE = "avatar/currentResponse.txt"

# Ensure directories exist
os.makedirs(LOGS_DIRECTORY, exist_ok=True)
os.makedirs(CONTEXT_DIR, exist_ok=True)
os.makedirs(os.path.dirname(TERMINAL_COMMANDS_FILE), exist_ok=True)
os.makedirs(os.path.dirname(CURRENT_RESPONSE_FILE), exist_ok=True)