from utils.file_operations import load_initial_context, read_file, write_file, install_package
from utils.git_operations import get_off_dev_branch, load_project_git, avatar_commit_git, avatar_push_git
from utils.responseParser import parse_llm_response
import sys
import os
from anthropic import Anthropic
import site

SYSTEM_PROMPT = read_file("avatar/context/response_instructions.txt")
MAX_LLM_ITERATIONS = 14
LARGE_LANGUAGE_MODEL = Anthropic(api_key=os.environ.get('CLAUDE'))
MODEL_NAME = "claude-3-sonnet-20240229"
GH_USERNAME = os.environ.get('GH_USERNAME')


# Add user site-packages to Python path
user_site_packages = site.getusersitepackages()
sys.path.append(user_site_packages)

print(user_site_packages)
print(os.listdir(user_site_packages))


def main():

    print("@greatsun-dev reading you loud and clear")
    get_off_dev_branch()
    conversation_thread = load_initial_context()
    write_file("avatar/context/conversation_thread.txt", conversation_thread)
    print(f"*** MESSAGE FROM DEVELOPER @{GH_USERNAME} ***\n")

    while True:
        terminal_input = input().strip()

        if terminal_input.lower() == "avatar up":
            conversation_thread = load_initial_context()
            write_file("avatar/context/conversation_thread.txt",
                       conversation_thread)
            print(f"*** MESSAGE FROM DEVELOPER @{GH_USERNAME} ***\n")
            continue

        if terminal_input.lower() == "avatar load":
            load_branch = input("Project branch or `dev`: ")
            load_project_git(load_branch)
            continue

        if terminal_input.lower() == "avatar engage":
            print("engaged placeholder")
            continue

        if terminal_input.lower() == "avatar commit":
            avatar_commit_git()
            continue

        if terminal_input.lower() == "avatar push":
            project_branch = input("Project branch: ")
            avatar_push_git(project_branch)
            continue

        if terminal_input.lower() == "avatar down":
            print("greatsun-dev, signing off")
            break

        # Add new terminal message to conversation
        conversation_thread = read_file(
            "avatar/context/conversation_thread.txt")
        conversation_thread += f"\n\n*** MESSAGE FROM DEVELOPER @{GH_USERNAME} ***\n\n{
            terminal_input}"
        write_file("avatar/context/conversation_thread.txt",
                   conversation_thread)

        # START LLM LOOP, allow to run up to MAX_LLM_ITERATIONS iterations
        for iteration in range(MAX_LLM_ITERATIONS):
            try:
                llm_message = conversation_thread
                print(f"avatar iteration {
                      iteration + 1} of up to {MAX_LLM_ITERATIONS}")

                llm_call = LARGE_LANGUAGE_MODEL.messages.create(
                    model=MODEL_NAME,
                    max_tokens=4096,
                    temperature=0,
                    system=SYSTEM_PROMPT,
                    messages=[
                        {"role": "user", "content": llm_message}
                    ]
                )
                llm_response = llm_call.content[0].text
                conversation_thread += f"\n\n*** LLM RESPONSE ***\n\n{
                    llm_response}"

                # Process the LLM response
                conversation_thread, developer_input_required, terminal_output = parse_llm_response(
                    conversation_thread, llm_response)

                print(terminal_output)

                if developer_input_required:
                    print(f"\n*** MESSAGE FROM DEVELOPER @{GH_USERNAME} ***")
                    break

                # TESTING REMOVING THIS
                # If no developer input is required, but there's no more to do, also break
                # if not terminal_output.strip():
                    # print("\n*** DEVELOPER REPONSE ***")
                    # break

                # If there are more actions to perform, continue to the next iteration
                # print("Continuing to next iteration")
                # logger.info("Continuing to next iteration")

            except anthropic.APIError as e:
                print(f"Anthropic API error in LLM iteration {
                    iteration + 1}: {str(e)}")
                print(f"An error occurred with the Anthropic API in LLM iteration {
                      iteration + 1}:")
                print(str(e))
                print("Please check the logs for more details.")
                break
            except Exception as e:
                print(f"Error in LLM iteration {
                    iteration + 1}: {str(e)}")
                print(f"An unexpected error occurred in LLM iteration {
                      iteration + 1}:")
                print(str(e))
                print("Please check the logs for more details.")
                break

        else:
            # This block executes if the for loop completes without breaking
            final_response = "The LLM reached the maximum number of iterations without completing the task. Let's try again or consider rephrasing the request."
            print("LLM reached maximum iterations without completion")
            conversation_thread += f"\n\n{final_response}"
            write_file("avatar/context/conversation_thread.txt",
                       conversation_thread)
            print(final_response)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nOperation interrupted by user. Exiting gracefully.")
    except Exception as e:
        print(f"Critical error in main execution: {str(e)}")
        print("A critical error occurred in the main execution:")
        print(str(e))
        print("Please check the logs for more details.")
