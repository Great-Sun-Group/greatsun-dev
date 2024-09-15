# **Current Avatar Instructions from Developer**

instead of importing from the context_summary.json file, I want to import the logs from the last 15 minutes to add as context to the message sent to the ai. the logs are in the file avatar/context/conversationLog, named like: 2024-9-15.log and here is an example from the log:
**********
2024-09-15 01:01:30,475 - Content written to avatar/context/responseReceived.txt
2024-09-15 01:01:30,475 - No valid JSON found in the response.
2024-09-15 01:09:15,142 - File not found: avatar/responseInstructions.md
2024-09-15 01:09:15,149 - File not found: avatar/responseInstructions.md
2024-09-15 01:09:15,150 - Content written to avatar/context/messageSent.txt
2024-09-15 01:09:27,233 - File: /workspaces/greatsun-dev/avatar/avatarUp.py
2024-09-15 01:09:27,233 - Avatar: ```json
{
  "response": "The logging processes in this file seem to be well structured and comprehensive. The setup_logger() function creates a logger that writes logs to a daily log file in the avatar/context/conversationLog directory, as well as to the console for error messages. Logs include timestamps and log level information.\n\nThe read_file_content() and write_to_file() functions handle reading and writing file contents, respectively, with proper error handling and logging.\n\nThe read_summary_of_context() and write_summary_of_context() functions handle reading and writing the context summary JSON file, creating an empty file if it doesn't exist.\n\nThe get_directory_tree() function recursively gets the directory structure of the specified root directory, which is used to provide context to the AI system.\n\nThe extract_json_from_response() function extracts JSON data from the AI response, if present, and separates it from the remaining text.\n\nThe process_ai_response() function handles the different components of the AI response JSON, such as updating files, updating the context summary, writing terminal commands, and saving the response text.\n\nOverall, the logging processes seem to be well-designed and cover various aspects of the application's execution. However, if you have any specific concerns or requirements, please let me know.",
  "context_summary": [
    {
      "summary": "The script has been updated to extract terminal commands and AI responses from the JSON response and save them to separate files."
    }
  ]
}
```

The logging processes in the provided code seem to be comprehensive and well-structured. Here are some observations:

1. **Logger Setup**: The `setup_logger()` function creates a logger instance with appropriate configurations. It sets the log level to `INFO` and creates file and console handlers. Log messages are written to a daily log file in the `avatar/context/conversationLog` directory, and error messages are also printed to the console.

2. **File Operations**: The `read_file_content()` and `write_to_file()` functions handle reading and writing file contents, respectively. They include error handling and logging for various exceptions that may occur during file operations.

3. **Context Summary Management**: The `read_summary_of_context()` and `write_summary_of_context()` functions handle reading and writing the context summary JSON file. If the file doesn't exist, an empty file is created.

4. **Directory Structure**: The `get_directory_tree()` function recursively retrieves the directory structure of the specified root directory. This is likely used to provide context to the AI system about the project's file structure.

5. **JSON Extraction**: The `extract_json_from_response()` function attempts to extract JSON data from the AI response. If JSON is found, it separates the JSON data from the remaining text.

6. **Response Processing**: The `process_ai_response()` function handles different components of the AI response JSON. It can update files, update the context summary, write terminal commands, and save the response text to separate files.

Overall, the logging processes seem well-designed and cover various aspects of the application's execution, including file operations, context management, and response handling. However, if you have any specific concerns or requirements, please let me know.
2024-09-15 01:09:27,233 - Content written to avatar/context/responseReceived.txt
2024-09-15 01:09:27,234 - Summary of context updated
2024-09-15 01:09:27,234 - Context summary updated
2024-09-15 01:09:27,234 - Content written to avatar/currentResponse
2024-09-15 01:09:27,234 - Response written to 'avatar/currentResponse'
**********
we need to update the read_summary_of_context function here to implement the above