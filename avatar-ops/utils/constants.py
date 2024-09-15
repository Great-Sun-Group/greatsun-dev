import os

API_KEY = os.getenv("CLAUDE")
if not API_KEY:
    raise ValueError("CLAUDE API key not found in environment variables")

LOGS_DIRECTORY = "avatar-ops/context/conversationLog"
RESPONSE_INSTRUCTIONS = "avatar-ops/context/responseInstructions.md"
AVATAR_README = "avatarREADME.md"
README = "README.md"
MESSAGE_TO_SEND = "avatar-ops/messageToSend.md"
CONTEXT_DIR = "avatar-ops/context"
TERMINAL_COMMANDS_FILE = "avatar-ops/terminalCommands.txt"
CURRENT_RESPONSE_FILE = "avatar-ops/context/currentResponse.txt"

# Ensure directories exist
os.makedirs(LOGS_DIRECTORY, exist_ok=True)
os.makedirs(CONTEXT_DIR, exist_ok=True)
os.makedirs(os.path.dirname(TERMINAL_COMMANDS_FILE), exist_ok=True)
os.makedirs(os.path.dirname(CURRENT_RESPONSE_FILE), exist_ok=True)