import os
import requests

# Get environment variables
token = os.environ['SECRET_TOKEN']
repository = "mk-mahina/PR-Merge-DryRun"
issue_number = '6'
assignee = 'armin-mahina'

# Set API URL
url = f"https://api.github.com/repos/{repository}/issues/{issue_number}/assignees"

# Set payload
payload = {
    "assignees": [assignee]
}

# Set headers
headers = {
    "Accept": "application/vnd.github.v3+json",
    "Authorization": f"token {token}"
}

# Send POST request
response = requests.post(url, headers=headers, json=payload)

# Print response
print(response.text)
