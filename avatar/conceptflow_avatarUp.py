import json
import os
import logging
import re
from anthropic import Anthropic
from avatarUpCommands import cross_repo_commit
from utils import read_file, write_file, get_directory_tree

# Configure logging
logging.basicConfig(filename='avatar.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Constants
ANTHROPIC_API_KEY = os.environ.get('CLAUDE')
GITHUB_USERNAME = os.environ.get('GITHUB_USERNAME')
MAX_LLM_ITERATIONS = 42
MODEL_NAME = "claude-3-5-sonnet-20240620"

# Initialize Anthropic client
try:
    large_language_model = Anthropic(api_key=ANTHROPIC_API_KEY)
    greatsun_developer = GITHUB_USERNAME
except Exception as e:
    logger.error(f"Failed to initialize Anthropic client: {str(e)}")
    raise


def extract_file_operation(response, operation):
    """
    Extract file operation details from LLM response.

    Args:
    response (str): LLM response
    operation (str): Either 'READ_FILE' or 'WRITE_FILE'

    Returns:
    tuple: (file_path, file_contents) for WRITE_FILE, or (file_path, None) for READ_FILE
    """
    if operation == 'READ_FILE':
        pattern = r"READ_FILE\n(.*?)\n"
    elif operation == 'WRITE_FILE':
        pattern = r"WRITE_FILE\n(.*?)\n<--write_file_start-->\n(.*?)\n<--write_file_end-->"
    else:
        logger.error(f"Invalid operation: {operation}")
        return None, None

    match = re.search(pattern, response, re.DOTALL)
    if match:
        if operation == 'READ_FILE':
            return match.group(1), None
        else:
            return match.group(1), match.group(2)
    return None, None


def process_llm_response(llm_response):
    """
    Process the LLM response and perform file operations.

    Args:
    llm_response (str): Response from the LLM

    Returns:
    str: Processed response for the developer
    """
    read_path, _ = extract_file_operation(llm_response, 'READ_FILE')
    write_path, write_contents = extract_file_operation(
        llm_response, 'WRITE_FILE')

    conversation = read_file("avatar/avatarConversation.txt")

    if read_path:
        try:
            read_data = f"READ_FILE\n{read_path}\n{read_file(read_path)}"
            conversation += f"\n\n{read_data}"
            logger.info(f"Read file: {read_path}")
        except Exception as e:
            logger.error(f"Failed to read file {read_path}: {str(e)}")

    if write_path and write_contents:
        try:
            write_file(write_path, write_contents)
            conversation += f"\n\nWRITE_FILE\n{write_path}\n{write_contents}"
            logger.info(f"Wrote file: {write_path}")
        except Exception as e:
            logger.error(f"Failed to write file {write_path}: {str(e)}")

    write_file("avatar/avatarConversation.txt", conversation)

    # Remove file operation patterns from the response
    response_to_developer = re.sub(
        r"(READ_FILE|WRITE_FILE).*?(<--write_file_end-->)?", "", llm_response, flags=re.DOTALL)
    return response_to_developer.strip()


def main():
