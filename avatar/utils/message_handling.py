from typing import Optional, List
import json
import os
from .constants import RESPONSE_INSTRUCTIONS, AVATAR_README, README, MESSAGE_TO_SEND
from .file_operations import read_file_content, read_recent_logs, get_directory_tree

def get_message_content(file_path: str, included_content: Optional[str], requested_files: List[str] = None) -> str:
    content_parts = [
        read_file_content(RESPONSE_INSTRUCTIONS),
        read_file_content(AVATAR_README),
        read_file_content(README),
        "IMPORTANT IMPORTANT IMPORTANT",
        "# **Current Instructions from Developer**",
        read_file_content(MESSAGE_TO_SEND),
        f"## Summary of context\n\n## Attached path\n{file_path}" if file_path else None,
        f"### Attached path contents\n{included_content}" if included_content else None,
    ]

    if requested_files:
        for file in requested_files:
            full_path = os.path.join('/workspaces/greatsun-dev', file.strip('"{}'))
            content = read_file_content(full_path)
            content_parts.append(f"### Contents of {file}\n{content}" if content else f"### File {file} not found or empty")

    content_parts.extend([
        f"### Last 15 minutes of logs\n{read_recent_logs(minutes=15)}",
        f"### Directory structure\n{json.dumps(get_directory_tree('/workspaces/greatsun-dev'), indent=2)}",
        read_file_content(RESPONSE_INSTRUCTIONS)
    ])

    return "\n\n".join(filter(None, content_parts))