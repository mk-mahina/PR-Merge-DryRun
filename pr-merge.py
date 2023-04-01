import os
import requests

# Get environment variables
token = os.environ['SECRET_TOKEN']
repository = "mk-mahina/PR-Merge-DryRun"
pull_number = os.environ['PULL_NUMBER']

# Set API URLs
pr_url = f"https://api.github.com/repos/{repository}/pulls/{pull_number}"
reviews_url = f"{pr_url}/reviews"
assignees_url = f"https://api.github.com/repos/{repository}/issues/{pull_number}/assignees"

# Set headers
headers = {
    "Accept": "application/vnd.github.v3+json",
    "Authorization": f"token {token}"
}

# Check if the pull request is approved
pr_response = requests.get(pr_url, headers=headers)
pr_data = pr_response.json()
if pr_data["state"] != "open":
    print("PR is not open. Exiting.")
    exit(0)
reviews_response = requests.get(reviews_url, headers=headers)
reviews_data = reviews_response.json()
approvals = [review for review in reviews_data if review["state"] == "APPROVED"]
if not approvals:
    print("No approvals found. PR not assigned.")
    exit(0)

# Remove existing assignees
existing_assignees_response = requests.get(assignees_url, headers=headers)
existing_assignees_data = existing_assignees_response.json()
existing_assignees = existing_assignees_data["assignees"]
for assignee in existing_assignees:
    remove_assignee_url = f"https://api.github.com/repos/{repository}/issues/{pull_number}/assignees/{assignee['login']}"
    remove_assignee_response = requests.delete(remove_assignee_url, headers=headers)
    if remove_assignee_response.ok:
        print(f"Assignee {assignee['login']} removed.")
    else:
        print(f"Failed to remove assignee {assignee['login']}. Response: {remove_assignee_response.text}")

# Assign the pull request to "armin-mahina"
assignees_payload = {
    "assignees": ["armin-mahina"]
}
assignees_response = requests.post(assignees_url, headers=headers, json=assignees_payload)
if assignees_response.ok:
    print("PR assigned to armin-mahina.")
else:
    print(f"Failed to assign PR to armin-mahina. Response: {assignees_response.text}")
