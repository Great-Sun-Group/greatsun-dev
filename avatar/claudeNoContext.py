import logging
import os
from datetime import datetime
from anthropic import Anthropic

# Get the API key from the environment variable
api_key = os.getenv('CLAUDE')

# Create a logs directory if it doesn't exist
logs_directory = 'conversationLog'
os.makedirs(logs_directory, exist_ok=True)

# Create a logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Create a file handler for the logger
current_date = datetime.now().strftime('%Y-%m-%d')
log_file = f'{logs_directory}/{current_date}.log'
file_handler = logging.FileHandler(log_file)
file_handler.setLevel(logging.INFO)

# Create a formatter and add it to the file handler
formatter = logging.Formatter('%(asctime)s - %(message)s')
file_handler.setFormatter(formatter)

# Add the file handler to the logger
logger.addHandler(file_handler)

# Initialize Anthropic client
client = Anthropic(api_key=api_key)

def read_file_content(file_path):
    try:
        with open(file_path, 'r') as file:
            return file.read()
    except Exception as e:
        logger.error(f'Error reading file: {e}')
        return None

while True:
    user_input = input('User: ')

    if user_input.lower() == 'exit':
        print('Goodbye!')
        break

    file_path = input('Optional file path (press Enter to skip): ').strip()

    message_content = user_input
    message_content += f'Return your response in the form of a full file that can be copied and pasted into the project, replacing the file that is currently there.'

    if file_path:
        file_content = read_file_content(file_path)
        if file_content:
            message_content += f'\\n\nHere\'s the content of the file at {file_path}:\\n\\n{file_content}\\n\\nPlease consider this file content in your response.'

    # Send user input and optional file content to Anthropic API
    message = client.messages.create(
        model='claude-3-opus-20240229',
        max_tokens=2000,
        messages=[
            {'role': 'user', 'content': message_content}
        ]
    )

    ai_response = message.content[0].text

    print(f'AI: {ai_response}')

    logger.info(f'User: {user_input}')
    if file_path:
        logger.info(f'File: {file_path}')
    logger.info(f'AI: {ai_response}')