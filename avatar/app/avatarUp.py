import os
import sys
import site
from anthropic import Anthropic
from config import BASE_DIR, GH_USERNAME
from basics import write_file, read_file, load_initial_context, get_off_dev_and_project_branch, get_current_branch
from load_project_git import load_project_git
from avatar_commit_git import avatar_commit_git
from avatar_submit_git import avatar_submit_git
from response_parser import llm_response_for_developer, parse_llm_response
from dev_run_servers import dev_run_servers

LARGE_LANGUAGE_MODEL = Anthropic(api_key=os.environ.get('CLAUDE'))
MAX_LLM_ITERATIONS = 14
MODEL_NAME = "claude-3-sonnet-20240229"

# Add user site-packages to Python path
user_site_packages = site.getusersitepackages()
sys.path.append(user_site_packages)


def main():
    print(f"\n@greatsun-dev reading you loud and clear")
    get_off_dev_and_project_branch()
    conversation_thread = read_file(
        BASE_DIR / "avatar/conversation_thread.txt")
    print(f"\n\n*** MESSAGE FROM DEVELOPER @{GH_USERNAME} ***\n")

    while True:
        terminal_input = input().strip()

        if terminal_input.lower() == "avatar refresh":
            conversation_thread = load_initial_context()
            write_file(BASE_DIR / "avatar/conversation_thread.txt",
                       conversation_thread)
            print(f"\n\n*** MESSAGE FROM DEVELOPER @{GH_USERNAME} ***\n")
            continue

        if terminal_input.lower() == "avatar load":
            load_branch = input("Project branch or `dev`: ")
            try:
                load_project_git(load_branch)
            except Exception as e:
                print(f"Error loading project: {str(e)}")
                print("Traceback:")
                import traceback
                traceback.print_exc()
            continue

        if terminal_input.lower() == "avatar engage":
            dev_run_servers()
            continue

        if terminal_input.lower() == "avatar commit":
            avatar_commit_git()
            continue

        if terminal_input.lower() == "avatar submit":
            project_branch = input("Project branch: ")
            avatar_submit_git(project_branch)
            continue

        if terminal_input.lower() == "avatar down":
            current_branch = get_current_branch()
            print(f"\ngreatsun-dev signing off branch {current_branch}")
            break

        # Add new terminal message to conversation
        conversation_thread += f"{terminal_input}"
        write_file(BASE_DIR / "avatar/conversation_thread.txt",
                   conversation_thread)

        # START LLM LOOP, allow to run up to MAX_LLM_ITERATIONS iterations
        for iteration in range(MAX_LLM_ITERATIONS):
            try:
                llm_message = conversation_thread
                print(
                    f"\n\n*** AVATAR RESPONSE {iteration + 1} OF UP TO {MAX_LLM_ITERATIONS} ***\n")

                llm_call = LARGE_LANGUAGE_MODEL.messages.create(
                    model=MODEL_NAME,
                    max_tokens=4096,
                    temperature=0,
                    system=read_file(
                        BASE_DIR / "avatar/app/response_instructions.txt"),
                    messages=[
                        {"role": "user", "content": llm_message}
                    ]
                )
                llm_response = llm_call.content[0].text
                conversation_thread += f"\n\n*** LLM RESPONSE ***\n\n{
                    llm_response}\n\n*** AUTOMATED RESPONSE TO ANY FILE OPERATIONS REQUESTED ***\n\n"

                # Trim the file contents out of the response and print the rest for the developer
                llm_for_developer = llm_response_for_developer(llm_response)
                print(llm_for_developer)

                # Process the LLM response
                developer_input_required, updated_conversation_thread = parse_llm_response(
                    llm_response, conversation_thread)

                # Update conversation_thread with the result from parse_llm_response
                conversation_thread = updated_conversation_thread

                # Write the updated conversation thread to file
                write_file(BASE_DIR / "avatar/conversation_thread.txt",
                           conversation_thread)

                if developer_input_required:
                    conversation_thread += f"\n*** MESSAGE FROM DEVELOPER @{
                        GH_USERNAME} ***\n"
                    write_file(
                        BASE_DIR / "avatar/conversation_thread.txt", conversation_thread)
                    print(
                        f"\n\n*** MESSAGE FROM DEVELOPER @{GH_USERNAME} ***\n")
                    break

            except Exception as e:
                print(f"Error in LLM iteration {iteration + 1}: {str(e)}")
                print("Please check the logs for more details.")
                conversation_thread += f"\n\nError in LLM iteration {
                    iteration + 1}: {str(e)}"
                write_file(BASE_DIR / "avatar/conversation_thread.txt",
                           conversation_thread)
                break

        else:
            # This block executes if the for loop completes without breaking
            final_response = "The LLM reached the maximum number of iterations without completing the task. Let's try again or consider rephrasing the request."
            print("LLM reached maximum iterations without completion")
            conversation_thread += f"\n\n{final_response}"
            write_file(BASE_DIR / "avatar/conversation_thread.txt",
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
        print("Error type:", type(e).__name__)
        import traceback
        print("Traceback:")
        traceback.print_exc()
