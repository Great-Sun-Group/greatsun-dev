import json
import os
from typing import Optional, Dict, Any, List, Tuple
from .constants import CURRENT_RESPONSE_FILE
from .file_operations import write_to_file, read_file_content, logger


def process_ai_response(response_json: Optional[Dict[str, Any]], remaining_text: str) -> Tuple[List[str], bool, List[str]]:
    logger.debug(
        f"Entering process_ai_response with response_json: {response_json}")

    requested_files = []
    actions_recommended = False
    additional_files_to_update = []

    if response_json:
        logger.info(
            f"Processing AI response: {json.dumps(response_json, indent=2)}")

        # Read existing response
        existing_response = read_file_content(CURRENT_RESPONSE_FILE)

        # Handle response
        response_text = response_json.get("response", "")
        if remaining_text:
            response_text += f"\n\nAdditional information:\n{remaining_text}"

        # Append new response to existing response
        updated_response = f"{existing_response}\n\nNew response:\n{response_text}"
        write_to_file(CURRENT_RESPONSE_FILE, updated_response)

        # Handle file requests (keeping the existing loop)
        for i in range(1, 8):
            file_key = f"file_requested_{i}"
            if file_key in response_json:
                requested_files.append(response_json[file_key].strip('"{}'))

        if requested_files:
            logger.info(f"Files requested: {', '.join(requested_files)}")

        # Handle file updates
        update_file_path = response_json.get("update_file_path")
        update_file_contents = response_json.get("update_file_contents")

        if update_file_path and update_file_contents:
            try:
                abs_file_path = os.path.abspath(update_file_path.strip('"{}'))
                logger.info(f"Attempting to update file: {abs_file_path}")
                if isinstance(update_file_contents, dict):
                    content = json.dumps(update_file_contents, indent=2)
                else:
                    content = str(update_file_contents)
                write_to_file(abs_file_path, content)
                actions_recommended = True
            except Exception as e:
                logger.error(
                    f"Failed to update file {abs_file_path}: {str(e)}")
        else:
            logger.info("No file update information provided in the response.")

        # Handle additional files to update
        additional_files = response_json.get("additional_files_to_update")
        if additional_files:
            if isinstance(additional_files, list):
                additional_files_to_update = additional_files
            elif isinstance(additional_files, str):
                additional_files_to_update = [additional_files]
            logger.info(
                f"Additional files to update: {additional_files_to_update}")

        # Set actions_recommended to True if there are file updates, additional files, or requested files
        if update_file_path or additional_files_to_update or requested_files:
            actions_recommended = True

    else:
        logger.warning("No valid JSON found in the response.")
        # Append remaining text to existing response
        existing_response = read_file_content(CURRENT_RESPONSE_FILE)
        updated_response = f"{existing_response}\n\nAdditional information:\n{remaining_text}"
        write_to_file(CURRENT_RESPONSE_FILE, updated_response)

    logger.debug("Exiting process_ai_response")
    return requested_files, actions_recommended, additional_files_to_update
