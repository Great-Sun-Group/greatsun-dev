I want to update the attached script to interact with the AI according to these response instructions sent to the AI

# AI response instructions !IMPORTANT!

## You have the option to respond to this query in one of two ways:
1. With an array of file paths (up to 10) that you would like to review to receive more information
    - if you respond in this way, we will append the contents of the files requested to this message and resend it so that you have the context that you need.
2. With the json described below and throught the rest of this message.
    - respond in this way when you are ready to recommend actions (file changes or terminal commands)

You will need to decide if you have enough information from this request to go to response 2 above, or if you need more context and therefore want to use response 1.

## Option 2: returning json to be parsed and acted on

If you respond in json (option 2 above) then **your responses will be parsed before being displayed**, and you are required to send data in a format that enables us to easily act on your recommendations. It is *very important* that you **respond to this query in json**, in these key/value pairs, so that we can parse your response correctly, and understand each other.

{
  "response": "your response here in english for us to read",
  "context_summary": "state of the current tasks"
  "terminal_command": "terminal commands that you recommend we execute here",
  "update_file_path_1": "the path of the file that you recommend that we update",
  "update_file_contents_1": "complete file contents here of the first file you recommend that we update",
  "update_file_path_2": "path of a second file that you recommend that we update",
  "update_file_contents_2": "complete file contents here of the second file you recommend that we update",
  "update_file_path_3": "path of a third file that you recommend that we update",
  "update_file_contents_3": "complete file contents here of the third file you recommend that we update",
  "update_file_path_4": "path of a fourth file that you recommend that we update",
  "update_file_contents_4": "complete file contents here of the fourth file you recommend that we update",
  "update_file_path_5": "path of a fifth file that you recommend that we update",
  "update_file_contents_5": "complete file contents here of the fifth file you recommend that we update",
}

DO not include anything in your response except the json above. Anything that you want to put outside the json, instead include it in response. We will process different portions of your response into different files and action paths, so be certain to always respond as above. 

### Required fields that must be included in every response:
- response
- context_summary

### Optional fields that can be included as needed:
- update_file_path_1
- update_file_contents_1
- update_file_path_2
- update_file_contents_2
- update_file_path_3
- update_file_contents_3
- update_file_path_4
- update_file_contents_4
- update_file_path_5
- update_file_contents_5