# AI response instructions !IMPORTANT!

## You have the option to respond to this query in one of two ways:

**Your responses will be parsed before being displayed**, so you are required to send data in a format that we can process to act on your recommendations or provide you with additional context. It is *very important* that you **respond to this message with json in one of the two ways below.**

DO not include anything in your response except the json below. Anything that you want to put outside the json, instead include it in response. We will process different portions of your response into different files and action paths, so be certain to always respond as above. 


## Option 1: request more context with json
Respond with json indicating that you would like to review to receive more information. If you respond in this way, we will append the contents of the files requested to this message and resend it so that you have all the context that you need. For example:
{
  "response": "Thank you for the instructions and context provided. To better understand how to assist, I would like to review these relevant files.",
  "file_requested_1": "avatar/utils.py"
  "file_requested_2": "README.md"
  "file_requested_3": "avatar/detDirectoryTree.py"
}

## Option 2: recommed actions with json
Respond in this way when you have enough context to confidently recommend actions (file changes or terminal commands)
{
  "response": "Your response to the query, including any information that the developer needs to know about the actions you are recommending.",
  "terminal_command": "put any terminal commands that you recommend we execute here",
  "update_file_path_1": "the path of the file that you recommend that we update",
  "update_file_contents_1": "The full updated contents of the first file to be updated, without any placeholders such as "remaining code unchanged" etc. This code will overwrite what is at the file path specified above, so it must be complete and correct to the best of your ability.",
  "update_file_path_2": "path of a second file that you recommend that we update",
  "update_file_contents_2": "The full updated contents of the second file to be updated, without any placeholders such as "remaining code unchanged" etc. This code will overwrite what is at the file path specified above, so it must be complete and correct to the best of your ability.",
  "update_file_path_3": "path of a third file that you recommend that we update",
  "update_file_contents_3": "The full updated contents of the third file to be updated, without any placeholders such as "remaining code unchanged" etc. This code will overwrite what is at the file path specified above, so it must be complete and correct to the best of your ability.",
  "update_file_path_4": "path of a fourth file that you recommend that we update",
  "update_file_contents_4": "The full updated contents of the fourth file to be updated, without any placeholders such as "remaining code unchanged" etc. This code will overwrite what is at the file path specified above, so it must be complete and correct to the best of your ability.",
  "update_file_path_5": "path of a fifth file that you recommend that we update",
  "update_file_contents_5": "The full updated contents of the fifth file to be updated, without any placeholders such as "remaining code unchanged" etc. This code will overwrite what is at the file path specified above, so it must be complete and correct to the best of your ability.",
}

### Required field that must be included in every response:
- response

### Optional fields that can be included as needed:
- update_file_path_[integer]
- update_file_contents_[integer]
- file_requested_[integer]

## Your decision
You will need to decide if you have enough information from this request to go to response 2 above, or if you need more context and therefore want to use response 1. Only choose one, and format your response according to the method chosen

### Important
Do not recommend updates to any file that has not been sent to you. If you need to recommend a file, first request it using option 1 above.