import json
import os
from typing import Optional, Dict, Any, List, Tuple
from .constants import CURRENT_RESPONSE_FILE
from .file_operations import write_to_file, logger


def process_ai_response(response_json: Optional[Dict[str, Any]], remaining_text: str) -> Tuple[List[str], bool, List[str]]:
    logger.debug(
        f"Entering process_ai_response with response_json: {response_json}")

    requested_files = []
    actions_recommended = False
    additional_files_to_update = []

    if response_json:
        logger.info(
            f"Processing AI response: {json.dumps(response_json, indent=2)}")

        # Handle response
        response_text = response_json.get("response", "")
        if remaining_text:
            response_text += f"\n\nAdditional information:\n{remaining_text}"
        write_to_file(os.path.join(
            os.getcwd(), CURRENT_RESPONSE_FILE), response_text)

        # Handle file requests
        for i in range(1, 8):
            file_key = f"file_requested_{i}"
            if file_key in response_json:
                requested_files.append(response_json[file_key].strip('"{}'))

        if requested_files:
            logger.info(f"Files requested: {', '.join(requested_files)}")
        else:
            actions_recommended = True

        # Handle file updates
        update_file_path = response_json.get("update_file_path")
        update_file_contents = response_json.get("update_file_contents")

        if update_file_path and update_file_contents:
            try:
                abs_file_path = os.path.abspath(update_file_path.strip('"{}'))
                logger.info(f"Attempting to update file: {abs_file_path}")
                write_to_file(abs_file_path, update_file_contents)
                actions_recommended = True
            except Exception as e:
                logger.error(
                    f"Failed to update file {abs_file_path}: {str(e)}")
        else:
            logger.info("No file update information provided in the response.")

    else:
        logger.warning("No valid JSON found in the response.")
        write_to_file(os.path.join(
            os.getcwd(), CURRENT_RESPONSE_FILE), remaining_text)

    logger.debug("Exiting process_ai_response")
    return requested_files, actions_recommended, additional_files_to_update


def extract_json_from_response(response: str) -> Tuple[Optional[Dict[str, Any]], str]:
    try:
        start = response.index('{')
        end = response.rindex('}') + 1
        json_str = response[start:end]
        json_data = json.loads(json_str)
        remaining_text = response[:start] + response[end:]
        return json_data, remaining_text.strip()
    except (ValueError, json.JSONDecodeError):
        logger.warning("No valid JSON found in the response.")
        return None, response
