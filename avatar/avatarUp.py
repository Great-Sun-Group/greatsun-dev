import json
import os
import logging
from anthropic import Anthropic
from avatarUpCommands import cross_repo_commit

# Configure logging
logging.basicConfig(filename='avatar.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Constants
ANTHROPIC_API_KEY = os.environ.get('CLAUDE')
GITHUB_USERNAME = os.environ.get('GITHUB_USERNAME')
MAX_LLM_ITERATIONS = 7

# Markers for parsing LLM responses
FINAL_MESSAGE_MARKER = "**@avatarParserSection: FINAL_RESPONSE_TO_DEVELOPER **"
UPDATE_FILE_MARKER = "**@avatarParserSection: FILE_TO_WRITE: "
REQUESTED_FILES_MARKER = "**@avatarParserSection: LIST_OF_FILES_REQUESTED_FOR_CONTEXT_BY_THE_LLM **"
PARSER_SECTION_END_MARKER = "**@avatarParserSection: SECTION_END **"

# Initialize Anthropic client
large_language_model = Anthropic(api_key=ANTHROPIC_API_KEY)
greatsun_developer = GITHUB_USERNAME


def read_file(file_path):
    """
    Robust function to read and return contents of a file, with solid error handling.
    If passed the path to a directory, it checks that it is a directory, logs that, and returns a message.

    Args:
    file_path (str): Path to the file or directory to be read

    Returns:
    str: Contents of the file or a message indicating it's a directory
    """
    try:
        if os.path.isdir(file_path):
            logging.info(f"Attempted to read directory: {file_path}")
            return "The reference is to a directory."

        with open(file_path, 'r') as file:
            content = file.read()
        logging.info(f"Successfully read file: {file_path}")
        return content
    except FileNotFoundError:
        logging.error(f"File not found: {file_path}")
        return f"Error: File not found - {file_path}"
    except PermissionError:
        logging.error(
            f"Permission denied when trying to read file: {file_path}")
        return f"Error: Permission denied - {file_path}"
    except Exception as e:
        logging.error(
            f"Unexpected error when reading file {file_path}: {str(e)}")
        return f"Error: Unexpected issue when reading file - {file_path}"


def write_file(file_path, file_content):
    """
    Robust function that will create the file if it doesn't exist and write over what is there if it does exist,
    with solid error handling.

    Args:
    file_path (str): Path to the file to be written
    file_content (str): Content to be written to the file

    Returns:
    bool: True if write operation was successful, False otherwise
    """
    try:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'w') as file:
            file.write(file_content)
        logging.info(f"Successfully wrote to file: {file_path}")
        return True
    except PermissionError:
        logging.error(
            f"Permission denied when trying to write to file: {file_path}")
        return False
    except Exception as e:
        logging.error(
            f"Unexpected error when writing to file {file_path}: {str(e)}")
        return False


def extract_content(text, start_marker, end_marker):
    """
    Extract content between two markers in a text.

    Args:
    text (str
