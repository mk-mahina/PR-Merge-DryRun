import os
import requests

# Get environment variables
token = os.environ['SECRET_TOKEN']
repository = "mk-mahina/PR-Merge-DryRun"
pull_number = os.environ['PULL_NUMBER']

# Set API URLs
pr_url = f"https://api.github.com/repos/{repository}/pulls/{pull_number}"
assignees_url = f"https://api.github.com/repos/{repository}/issues/{pull_number}/assignees"

# Set headers
headers = {
    "Accept": "application/vnd.github.v3+json",
    "Authorization": f"token {token}"
}

# Check if the pull request is approved
pr_response = requests.get(pr_url, headers=headers)
pr_data = pr_response.json()
reviews_url = pr_data["_links"]["reviews"]["href"]
reviews_response = requests.get(reviews_url, headers=headers)
reviews_data = reviews_response.json()
approvals = [review for review in reviews_data if review["state"] == "APPROVED"]
if not approvals:
    print("No approvals found. PR not assigned.")
    exit(0)

# Check if the pull request is already assigned to armin-mahina
assignees_response = requests.get(assignees_url, headers=headers)
assignees_data = assignees_response.json()
assignees = assignees_data.get("assignees", [])
if len(assignees) == 1 and assignees[0]["login"] == "armin-mahina":
    print("PR is already assigned to armin-mahina.")
    exit(0)

# Remove existing assignees
remove_assignees_url = assignees_url
if assignees:
    remove_assignees_payload = {
        "assignees": [assignee["login"] for assignee in assignees if assignee["login"] != "armin-mahina"]
    }
    remove_assignees_response = requests.delete(remove_assignees_url, headers=headers, json=remove_assignees_payload)
    if not remove_assignees_response.ok:
        print(f"Failed to remove existing assignees. Response: {remove_assignees_response.text}")
        exit(1)

# Assign the pull request to "armin-mahina"
assignees_payload = {
    "assignees": ["armin-mahina"]
}
assignees_response = requests.post(assignees_url, headers=headers, json=assignees_payload)
if assignees_response.ok:
    print("PR assigned to armin-mahina.")
else:
    print(f"Failed to assign PR to armin-mahina. Response: {assignees_response.text}")
