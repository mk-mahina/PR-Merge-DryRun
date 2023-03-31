import os
import requests
import json

os.environ['SECRET_TOKEN'] = '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'

pr_number = os.environ['PR_NUMBER']
github_token = os.environ['SECRET_TOKEN']
github_username = "armin-mahina"

print("PR_NUMBER:", pr_number)
print("SECRET_TOKEN:", github_token)
print("GITHUB_REPOSITORY:", os.environ['GITHUB_REPOSITORY'])
print(os.environ['SECRET_TOKEN'])
print(os.environ['PR_NUMBER'])
print(os.environ['GITHUB_REPOSITORY'])

url = f"https://api.github.com/repos/{os.environ['GITHUB_REPOSITORY']}/issues/{pr_number}/assignees"
headers = {
    "Accept": "application/vnd.github.v3+json",
    "Authorization": f"token {github_token}"
}
payload = {"assignees": [github_username]}

# Make a GET request to check if the PR is already assigned to the specified user
get_response = requests.get(url, headers=headers)
if get_response.status_code != 200:
    print("Error getting PR information:", get_response.json())
else:
    assignees = [assignee['login'] for assignee in get_response.json()['assignees']]
    print("Current assignees:", assignees)

    # Check if the user is already assigned to the PR
    if github_username in assignees:
        print(f"PR #{pr_number} is already assigned to {github_username}")
    else:
        # Make a POST request to assign the user to the PR
        post_response = requests.post(url, headers=headers, data=json.dumps(payload))
        if post_response.status_code != 201:
            print(f"Error assigning {github_username} to PR #{pr_number}:", post_response.json())
        else:
            print(f"{github_username} has been assigned to PR #{pr_number}")
