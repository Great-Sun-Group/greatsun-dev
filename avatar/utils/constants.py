import os

ANTHROPIC_API_KEY = os.getenv("CLAUDE")
LOGS_DIRECTORY = "avatar/context/logs"
RESPONSE_INSTRUCTIONS = "avatar/context/responseInstructions.md"
AVATAR_README = "avatar/context/avatarREADME.md"
README = "README.md"
MESSAGE_TO_SEND = "avatar/messageToSend.md"
CONTEXT_DIR = "avatar/context"
CURRENT_RESPONSE_FILE = "avatar/context/currentResponse.txt"

# Ensure directories exist
os.makedirs(LOGS_DIRECTORY, exist_ok=True)
os.makedirs(CONTEXT_DIR, exist_ok=True)
os.makedirs(os.path.dirname(CURRENT_RESPONSE_FILE), exist_ok=True)
