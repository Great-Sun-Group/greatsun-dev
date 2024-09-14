import logging
import os
from datetime import datetime
from anthropic import Anthropic

# Get the API key from the environment variable
api_key = os.getenv("CLAUDE")

# Create a logs directory if it doesn't exist
logs_directory = "conversationLog"
os.makedirs(logs_directory, exist_ok=True)

def setup_logger():
    # Create a logger
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)

    # Create a file handler for the logger
    current_date = datetime.now().strftime("%Y-%m-%d")
    log_file = f"{logs_directory}/{current_date}.log"
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(logging.INFO)

    # Create a formatter and add it to the file handler
    formatter = logging.Formatter('%(asctime)s - %(message)s')
    file_handler.setFormatter(formatter)

    # Add the file handler to the logger
    logger.addHandler(file_handler)

    return logger

# Initialize the logger
logger = setup_logger()

# Initialize Anthropic client
client = Anthropic(api_key=api_key)

def read_file_content(file_path):
    try:
        with open(file_path, 'r') as file:
            return file.read()
    except Exception as e:
        print(f"Error reading file: {e}")
        return None

def write_to_file(file_path, content):
    try:
        with open(file_path, 'w') as file:
            file.write(content)
        print(f"Content written to {file_path}")
    except Exception as e:
        print(f"Error writing to file: {e}")

while True:
    user_input = input("User: ")
    
    if user_input.lower() == "exit":
        print("Goodbye!")
        break
    
    file_path = input("Optional file path (press Enter to skip): ").strip()
    
    avatar_readme_content = read_file_content("avatarREADME.md")
    readme_content = read_file_content("README.md")
    message_to_send_content = read_file_content("messageToSend.txt")
    included_file_path = file_path
    included_file_content = read_file_content(file_path) if file_path else None
    
    message_content = ""
    if avatar_readme_content:
        message_content += avatar_readme_content + "\n\n"
    if readme_content:
        message_content += readme_content + "\n\n"
    
    if included_file_path:
        message_content += "# Attached file path \n"
        message_content += included_file_path + "\n"
        message_content += "# Attached file contents\n"
        if included_file_content:
            message_content += included_file_content + "\n"
    
    # Write the assembled message to messageSent.txt
    write_to_file("messageSent.txt", message_content)
    
    # Send user input and optional file content to Anthropic API
    message = client.messages.create(
        model="claude-3-opus-20240229",
        max_tokens=2000,
        messages=[
            {"role": "user", "content": message_content}
        ]
    )
    
    ai_response = message.content[0].text
    
    print(f"AI: {ai_response}")
    
    logger.info(f"User: {user_input}")
    if included_file_path:
        logger.info(f"File: {included_file_path}")
    logger.info(f"AI: {ai_response}")
    
    # Write AI response to responseReceived.txt
    write_to_file("responseReceived.txt", ai_response)
