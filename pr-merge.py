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
    status_response = requests.post(statuses_url, headers=headers, json=status_payload)
    if status_response.ok:
        print("Waiting for Manual Approval status check created.")
    else:
        print(f"Failed to create Waiting for Manual Approval status check. Response: {status_response.text}")
