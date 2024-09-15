# AI response instructions !IMPORTANT!

## You have the option to respond to this query in one of two ways:

**Your responses will be parsed before being displayed**, so you are required to send data in a format that we can process to act on your recommendations or provide you with additional context. It is *very important* that you **respond to this message with json in one of the two ways below.**

DO not include anything in your response except the json below. Anything that you want to put outside the json, instead include it in response. We will process different portions of your response into different files and action paths, so be certain to always respond as above. 


## Option 1: request more context with json
Respond with json indicating that you would like to review to receive more information, in the form of up to 7 files. You are not permitted to write over anything that you have not first read, so if you want to make changes to anything, request it.

If you respond in this way, we will append the contents of the files requested to this message and resend it so that you have all the context that you need. You can request more files if you need to recursively, up to a total of 7 times, enabling you to have up to 49 files sent to you for a single recommended update (proceeding to option 2 below). If you have files to request reply in this format, only sending as many file_requested key/values as you need, up to 7:
{
  "response": "To better understand how to assist, I would like to review these relevant files.",
  "file_requested_1": "avatar-ops/utils.py"
  "file_requested_2": "README.md"
  "file_requested_3": "avatar-ops/detDirectoryTree.py"
  "file_requested_4": "credex-ecosystem/credex-core/.gitignore"
  "file_requested_5": "credex-ecosystem/credex-core/placeholderFilame1.txt"
  "file_requested_6": "credex-ecosystem/credex-core/placeholderFilame2.txt"
  "file_requested_7": "credex-ecosystem/credex-core/placeholderFilame3.txt"
}

## Option 2: recommed an action with json
Respond using the template below when you have enough context to confidently recommend actions (file changes or terminal commands). The "response" field is always required, all others are optional.

If your workplan includes updates to more than one file, due to limits on response length, we will manage this with another call and response loop. Send your first recommended update, with the array of additional files to update in this workplan. Our script will make the file updates you suggest, append the changes to this message, along with the additional_files_to_update array that you sent it. If that array is included in this reponse, know there is work in progress that you are now focused on completing over multiple iterations.

- Your response will be displayed to your developer teammate.
- File changes youi send in this format will be made automatically for developer review, and you can iterate to make (recommend) changes to multiple files.
- Terminal commands must be copy pasted by a human developer, so no iterations are possible for those. Any terminal command sent in your response will end the loop, so don't add it if you have more files to update.

If you choose this Option 2, respond according to this template, and only within its structure.

{
  "response": "Your summary of the recomended actions, or your",
  "terminal_command": "put any terminal commands that you recommend we execute here",
  "update_file_path": "the path of the file that you recommend that we update",
  "update_file_contents": "The full updated contents of the file to be updated, without any placeholders such as "remaining code unchanged" etc. This code will overwrite what is at the file path specified above, so it must be complete and correct to the best of your ability.",
  "additional_files_to_update": "["path/of/first/file.txt","path/of/second/file.txt", "additional paths if needed]"
}

## Your decision
You will need to decide if there is enough information here for you to to recommend one or more actions, or if you need more context. If action is recommended, reply using the format in Option 2 above. If you need more context, reply using the format in Option 1 above. Only choose one formatting option based on your decision, and format your response according to the method chosen, with no additional data.