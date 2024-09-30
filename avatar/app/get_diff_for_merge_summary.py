import os
import requests
from config import GH_USERNAME, GH_PAT, GH_ORGANIZATION

def get_user_input():
    repo_name = input("Enter the repository name: ")
    from_branch = input("Enter the merge from branch name: ")
    into_branch = input("Enter the merge into branch name: ")
    return repo_name, from_branch, into_branch

def get_diff(repo_name, from_branch, into_branch):
    url = f"https://api.github.com/repos/{GH_ORGANIZATION}/{repo_name}/compare/{into_branch}...{from_branch}"
    headers = {
        "Authorization": f"token {GH_PAT}",
        "Accept": "application/vnd.github.v3.diff"
    }
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        return response.text
    else:
        return f"Error: {response.status_code} - {response.text}"

def filter_diff(diff_content):
    filtered_diff = []
    current_file = ""
    include_file = True
    
    for line in diff_content.split('\n'):
        if line.startswith('diff --git'):
            if current_file:
                if include_file:
                    filtered_diff.extend(current_file)
            current_file = [line]
            include_file = 'avatar/conversation_thread.txt' not in line
        elif include_file:
            current_file.append(line)
    
    if current_file and include_file:
        filtered_diff.extend(current_file)
    
    return '\n'.join(filtered_diff)

def write_diff_to_file(diff, filename):
    with open(filename, 'w') as f:
        f.write(diff)

def main():
    repo_name, from_branch, into_branch = get_user_input()
    diff = get_diff(repo_name, from_branch, into_branch)
    filtered_diff = filter_diff(diff)
    
    output_file = "/workspaces/greatsun-dev/avatar/app/generated_diff_report.txt"
    write_diff_to_file(filtered_diff, output_file)
    
    print(f"Filtered diff between {from_branch} and {into_branch} in {repo_name} has been saved to:")
    print(output_file)

if __name__ == "__main__":
    main()