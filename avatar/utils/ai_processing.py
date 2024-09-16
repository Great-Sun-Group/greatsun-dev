import json
import os
from typing import Optional, Dict, Any, List, Tuple
from .constants import CURRENT_RESPONSE_FILE
from .file_operations import write_to_file, write_terminal_command, logger

def process_ai_response(response_json: Optional[Dict[str, Any]], remaining_text: str) -> Tuple[List[str], bool, List[str]]:
    logger.debug(f"Entering process_ai_response with response_json: {response_json}")
    
    requested_files = []
    actions_recommended = False
    additional_files_to_update = []

    if response_json:
        logger.info(f"Processing AI response: {json.dumps(response_json, indent=2)}")

        # Handle response
        response_text = response_json.get("response", "")
        if remaining_text:
            response_text += f"\n\nAdditional information:\n{remaining_text}"
        write_to_file(os.path.join(os.getcwd(), CURRENT_RESPONSE_FILE), response_text)

        # Handle file requests
        for i in range(1, 8):
            file_key = f"file_requested_{i}"
            if file_key in response_json:
                requested_files.append(response_json[file_key].strip('"{}'))

        if requested_files:
            logger.info(f"Files requested: {', '.join(requested_files)}")
        else:
            actions_recommended = True

        # Handle terminal command
        terminal_command = response_json.get("terminal_command")
        if terminal_command:
            write_to_file(TERMINAL_COMMANDS_FILE, terminal_command + "\n")
            logger.info(f"Terminal command written: {terminal_command}")


        for i in range(1, 6):  # Assuming up to 5 file updates
            update_file_path = response_json.get(f"update_file_path_{i}")
            update_file_contents = response_json.get(f"update_file_contents_{i}")
            if update_file_path and update_file_contents:
                abs_file_path = os.path.abspath(update_file_path.strip('"{}'))
                logger.info(f"Attempting to update file: {abs_file_path}")
                write_to_file(abs_file_path, update_file_contents)
                actions_recommended = True
                # Handle additional files to update
                additional_files = response_json.get("additional_files_to_update")
                if additional_files:
                    additional_files_to_update = json.loads(additional_files) if isinstance(additional_files, str) else additional_files
                    logger.info(f"Additional files to update: {', '.join(additional_files_to_update)}")
                    actions_recommended = True
    else:
        logger.warning("No valid JSON found in the response.")
        write_to_file(os.path.join(os.getcwd(), CURRENT_RESPONSE_FILE), remaining_text)

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