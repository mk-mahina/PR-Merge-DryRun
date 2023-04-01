import os
import requests

# Get environment variables
token = os.environ['SECRET_TOKEN']
repository = "mk-mahina/PR-Merge-DryRun"
pull_number = os.environ['PULL_NUMBER']

# Set API URLs
pr_url = f"https://api.github.com/repos/{repository}/pulls/{pull_number}"
assignees_url = f"{pr_url}/assignees"

# Set headers
headers = {
    "Accept": "application/vnd.github.v3+json",
    "Authorization": f"token {token}"
}

# Check if the pull request is open
pr_response = requests.get(pr_url, headers=headers)
pr_data = pr_response.json()
if pr_data["state"] != "open":
    print("PR is not open. Exiting.")
    exit(0)

# Get existing assignees
assignees_response = requests.get(assignees_url, headers=headers)
assignees_data = assignees_response.json()
existing_assignees = [assignee['login'] for assignee in assignees_data]

# Remove existing assignees
if existing_assignees:
    assignees_payload = {
        "assignees": existing_assignees
    }
    assignees_response = requests.delete(assignees_url, headers=headers, json=assignees_payload)
    if assignees_response.ok:
        print("Existing assignees removed.")
    else:
        print(f"Failed to remove existing assignees. Response: {assignees_response.text}")
        
# Assign the pull request to "armin-mahina"
assignees_payload = {
    "assignees": ["armin-mahina"]
}
assignees_response = requests.post(assignees_url, headers=headers, json=assignees_payload)
if assignees_response.ok:
    print("PR assigned to armin-mahina.")
else:
    print(f"Failed to assign PR to armin-mahina. Response: {assignees_response.text}")
