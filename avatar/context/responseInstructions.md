# AI response instructions !IMPORTANT!

**Your responses will be parsed before being displayed**, and you are required to send data in a format that enables us to easily act on your recommendations. It is *very important* that you **respond to this query in json**, in these key/value pairs, so that we can parse your response correctly, and understand each other.

{
  "response": "your response here in english for us to read",
  "update_file_path": "the path of the file that you recommend that we update",
  "update_file_contents": "complete file contents here of the file you recommend that we update",
  "terminal_command": "terminal commands that you recommend we execute here",
  "context_summary": "state of the current tasks"
}

DO not include anything in your response except the json above. Anything that you want to put outside the json, instead include it in response. We will process different portions of your response into different files and action paths, so be certain to always respond as above. 

### Optional fields that can be included as needed:
- update_file_path
- update_file_contents
- terminal_command

### Required fields that must be included in every response:
- response
- context_summary