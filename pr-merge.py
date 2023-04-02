import os
import requests

# Get environment variables
token = os.environ['SECRET_TOKEN']
repository = "mk-mahina/PR-Merge-DryRun"
pull_number = os.environ['PULL_NUMBER']

# Set API URLs
pr_url = f"https://api.github.com/repos/{repository}/pulls/{pull_number}"
statuses_url = f"{pr_url}/statuses"

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

# Check if "Waiting for Manual Approval" status check already exists
statuses_response = requests.get(statuses_url, headers=headers)
statuses_data = statuses_response.json()
waiting_for_approval_statuses = [status for status in statuses_data if status["context"] == "Waiting for Manual Approval"]
if waiting_for_approval_statuses:
    print("Waiting for Manual Approval status check already exists.")
else:
    status_payload = {
        "state": "pending",
        "description": "This PR is waiting for manual approval",
        "context": "Waiting for Manual Approval"
    }
    create_status_response = requests.post(statuses_url, headers=headers, json=status_payload)
    if create_status_response.ok:
        print("Waiting for Manual Approval status check created.")
    else:
        print(f"Failed to create Waiting for Manual Approval status check. Response: {create_status_response.text}")
        exit(1)

# Check if "armin-mahina" has been added as a reviewer
reviewers_url = f"{pr_url}/requested_reviewers"
reviewers_response = requests.get(reviewers_url, headers=headers)
reviewers_data = reviewers_response.json()
if "armin-mahina" in [reviewer["login"] for reviewer in reviewers_data["users"]]:
    print("armin-mahina has been added as a reviewer.")
else:
    add_reviewer_url = f"{pr_url}/requested_reviewers"
    add_reviewer_payload = {
        "reviewers": ["armin-mahina"]
    }
    add_reviewer_response = requests.post(add_reviewer_url, headers=headers, json=add_reviewer_payload)
    if add_reviewer_response.ok:
        print("armin-mahina has been added as a reviewer.")
    else:
        print(f"Failed to add armin-mahina as a reviewer. Response: {add_reviewer_response.text}")
        exit(1)
