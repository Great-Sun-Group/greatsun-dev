Enhance this terminal interface between the developer and an AI assistant. These two fields should be optional:
- message
- file path

If a file path is provided, the script should attach the contents of the file and send it along with the message and path to the ai asisstant as three separate objects. At least one of the fields must be provided or error gracefully.

The AI assistant will process the user's input and know to respond with the following objects:
- a message (always)
- (optional) a file path and new file contents that the script inserts into that file, overwriting what was there or creating the file and associated directories if necessary
- (optional) a terminal command that gets saved to a specific file always on the project, overwriting whatever was there before, for the dev to edit and copypaste to the terminal.