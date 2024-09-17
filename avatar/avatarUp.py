import json
import os
import logging
from anthropic import Anthropic
from avatarUpCommands import cross_repo_commit

# Configure logging
logging.basicConfig(filename='avatar.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Constants
ANTHROPIC_API_KEY = os.environ.get('CLAUDE')
GITHUB_USERNAME = os.environ.get('GITHUB_USERNAME')
MAX_LLM_ITERATIONS = 42

# Initialize Anthropic client
large_language_model = Anthropic(api_key=ANTHROPIC_API_KEY)
greatsun_developer = GITHUB_USERNAME


def read_file(file_path):
    """
    Robust function to read and return contents of a file, with solid error handling.
    If passed the path to a directory, it checks that it is a directory, logs that, and returns a message.

    Args:
    file_path (str): Path to the file or directory to be read

    Returns:
    str: Contents of the file or a message indicating it's a directory
    """


def write_file(file_path, file_content):
    """
    Robust function that will create the file if it doesn't exist and write over what is there if it does exist,
    with solid error handling.

    Args:
    file_path (str): Path to the file to be written
    file_content (str): Content to be written to the file

    Returns:
    bool: True if write operation was successful, False otherwise
    """

def main():
    first_run = True
    """
    Main function to run the avatar environment.
    """
    os.system('cls' if os.name == 'nt' else 'clear')
    print("Welcome to the greatsun-dev avatar environment")
    print("Enter your instructions or questions in avatar/messageFromDeveloper.md")
    print("Then press enter here in the terminal, or you can first")
    print("optionally paste a file path as a starting point for my work")
    print(f"{greatsun_developer}: ")

    while True:
        file_path = input().strip()

        if file_path.lower() == "avatar down":
            print("\ngreatsun-dev avatar, signing off\n\n")
            break

        if file_path.lower() == "avatar commit":
            commit_id = cross_repo_commit()
            if commit_id:
                write_file("avatar/avatarConversation.txt",
                           "ready for conversation")
                print(f"Commit {commit_id} made and avatar cleared")
                continue

            if file_path.lower() == "avatar clear":
                write_file("avatar/avatarConversation.txt",
                           "ready for conversation")
                print("Avatar cleared")
                first_run = True  # Reset the flag when clearing
                continue

        # Prepare the message from the developer
        message_from_developer = read_file("avatar/messageFromDeveloper.md")
        reference_file_content = read_file(
            file_path) if file_path else "No reference file provided."
        trigger_message_content = f"{message_from_developer}\n\nReference File: {file_path}\n\n{reference_file_content}"

        if first_run:
            # Prepare the full context for the LLM (first run)
            avatar_up_content = [
                read_file("avatar/avatarOrientation.md"),
                read_file("avatar/avatarUp.py"),
                "** This is the project README.md **",
                read_file("README.md"),
                "** This is the credex-core submodule README.md **",
                read_file("credex-ecosystem/credex-core/README.md"),
                "** This is the vimbiso-pay submodule README.md **",
                read_file("credex-ecosystem/vimbiso-pay/README.md"),
                "** IMPORTANT IMPORTANT IMPORTANT: Current Instructions from Developer: the purpose of this conversation **",
                trigger_message_content,
                "Full Project Structure:",
                json.dumps(get_directory_tree(
                    '/workspaces/greatsun-dev'), indent=2),
                "** END avatarUp message **\n"
            ]
            avatar_up = "\n\n".join(avatar_up_content)
            write_file("avatar/avatarConversation.txt", avatar_up)
            first_run = False
        else:
            # For subsequent runs, append to existing conversation
            existing_conversation = read_file("avatar/avatarConversation.txt")
            updated_conversation = f"{existing_conversation}\n\n** New input from developer **\n\n{trigger_message_content}\n"
            write_file("avatar/avatarConversation.txt", updated_conversation)

        # START LLM LOOP, allow to run up to MAX_LLM_ITERATIONS iterations
        for iteration in range(MAX_LLM_ITERATIONS):
            try:
                llm_message = read_file("avatar/avatarConversation.txt")
                llm_call = large_language_model.messages.create(
                    model="claude-3-5-sonnet-20240620",
                    max_tokens=4096,
                    messages=[
                        {"role": "user", "content": llm_message}
                    ]
                )
                llm_response = llm_call.content[0].text
                conversationPlusResponse = llm_message, llm_response
                write_file("avatar/avatarConversation.txt",
                           conversationPlusResponse)

                # Process a requested file
                if the first line of the response is READ_A_FILE and the second line is a valid path argument(even if the file doesn't exist)
                   file_path_to_read = extract the second line
                   read_data = file_path_to_read + "\n" + read_file(file_path_to_read)
                    write_file("avatar/avatarConversation.txt" + "\n\n" +
                               conversationPlusResponse + "\n\n" + read_data)
                    print(
                        f"READ_A_FILE requested and sent: {file_path_to_read}")

                # Process a file update
                if the first line of the response is WRITE_A_FILE and the second line is a valid path argument
                    file_path_to_write = extract the second line
                    file_contents_to_write = the rest of the response
                    write_file(file_path_to_write, file_contents_to_write)
                    write_file("avatar/avatarConversation.txt",
                               conversationPlusResponse + "\n\n" + file_path_to_write + "\n" + file_contents_to_write)
                    print(
                        f"WRITE_A_FILE requested and written: {file_path_to_write}")

                # Extract response to developer
                if the first line of the response is RESPOND_TO_DEVELOPER
                   responseToDeveloper = extract everything past the first line
                    write_file("avatar/avatarResponseToDeveloper.md", responseToDeveloper)
                    write_file("avatar/avatarConversation.txt",
                               conversationPlusResponse + "\n\nRESPOND_TO_DEVELOPER:\n" + responseToDeveloper)

       else:
            # This block executes if the for loop completes without breaking
            final_response = "Sorry, the LLM we queried was unable to successfully complete the task. Let's try again, or consider using another model."
            avatar_conversation = read_file("avatar/avatarConversation.txt")
            write_file("avatar/avatarConversation.txt",
                       avatar_conversation + "\n\n" + final_response)
            print(final_response)

        # notify the developer
        print("\nAvatar response saved to avatar/avatarResponseToDeveloper.md")
        print("\nReady for next input. Type 'avatar down' to exit.")


if __name__ == "__main__":
    main()
