this script still doesn't reliable write to the various files.
fullResponseReceived works
currentResponse is the same as fullResponseReceived, but should be just the text of the response field, with any additional text outside of the json response from the ai appended, and that write should be to currentResponse.txt (add .txt)
terminalCommands.txt probably also is not getting saved, though I haven't tested
the last 15 minutes of logs is also not getting saved