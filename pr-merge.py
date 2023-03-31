import os
import requests
import json

# set up authentication using a Github access token
token = os.environ.get('GITHUB_TOKEN')
headers = {'Authorization': f'token {token}', 'Accept': 'application/vnd.github.v3+json'}

# get the Pull Request number and repository information from environment variables
pr_number = os.environ.get('PR_NUMBER')
repository = os.environ.get('GITHUB_REPOSITORY')

# get the Pull Request information using the Github API
url = f'https://api.github.com/repos/{repository}/pulls/{pr_number}'
response = requests.get(url, headers=headers)
pr_data = json.loads(response.text)

# check if the Pull Request is in an approved state
if pr_data['mergeable_state'] == 'clean' and pr_data['mergeable'] and pr_data['state'] == 'approved':

    # set the username of the user to assign the Pull Request to
    assignee = 'armin-mahina'

    # construct the API endpoint URL for assigning the Pull Request
    url = f'https://api.github.com/repos/{repository}/issues/{pr_number}/assignees'

    # make the API request to assign the Pull Request to the specified user
    response = requests.post(url, headers=headers, json={'assignees': [assignee]})

    # check the response status code to see if the request was successful
    if response.status_code == 201:
        print(f'Successfully assigned Pull Request #{pr_number} to {assignee}.')
    else:
        print(f'Failed to assign Pull Request #{pr_number} to {assignee}. Response status code: {response.status_code}.')
else:
    print(f'Pull Request #{pr_number} is not in an approved state and will not be assigned to {assignee}.')
