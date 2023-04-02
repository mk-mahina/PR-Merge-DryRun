import os
import requests

# Get environment variables
token = os.environ['SECRET_TOKEN']
repository = os.environ['GITHUB_REPOSITORY']
pull_number = os.environ['PULL_NUMBER']
review_gate_name = os.environ['REVIEW_GATE_NAME']

# Set API URLs
pr_url = f"https://api.github.com/repos/{repository}/pulls/{pull_number}"
statuses_url = f"{pr_url}/statuses"
reviews_url = f"{pr_url}/reviews"

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

# Check if the pull request is approved
reviews_response = requests.get(reviews_url, headers=headers)
reviews_data = reviews_response.json()

approved_reviewers = [review['user']['login'] for review in reviews_data if review['state'] == 'APPROVED']

if not approved_reviewers:
    print("PR is not approved. Exiting.")
    exit(0)

# Check if armin-mahina has been added as a reviewer
reviewers_response = requests.get(reviews_url, headers=headers)
reviewers_data = reviewers_response.json()

armin_reviewer = next((reviewer for reviewer in reviewers_data if reviewer['user']['login'] == 'armin-mahina'), None)

if armin_reviewer is None:
    review_payload = {
        "body": "Please review this PR",
        "event": "REQUEST_CHANGES",
        "reviewers": ["armin-mahina"]
    }
    review_response = requests.post(reviews_url, headers=headers, json=review_payload)
    if review_response.ok:
        print("armin-mahina has been added as a reviewer.")
    else:
        print(f"Failed to add armin-mahina as a reviewer. Response: {review_response.text}")
else:
    print("armin-mahina has already been added as a reviewer.")

# Check if the review gate status check already exists
statuses_response = requests.get(statuses_url, headers=headers)
statuses_data = statuses_response.json()

if "statuses" not in statuses_data:
    print(f"Error: statuses not found in response: {statuses_data}")
    exit(1)

review_gate_statuses = [status for status in statuses_data["statuses"] if status["context"] == review_gate_name]

if review_gate_statuses:
    print(f"{review_gate_name} status check already exists.")
else:
    # Check if another reviewer has approved the PR
    approved_reviewers = [review['user']['login'] for review in reviews_data if review['state'] == 'APPROVED' and review['user']['login'] != 'armin-mahina']

    if approved_reviewers:
        print(f"{approved_reviewers[0]} has already approved the PR. Skipping {review_gate_name} status check.")
    else:
        status_payload = {
            "state": "pending",
            "description": f"This PR is waiting for manual approval from armin-mahina before merging. ({review_gate_name})",
            "context": review_gate_name
        }
        status_response = requests.post(statuses_url, headers=headers, json=status_payload)
        if status_response.ok:
            print(f"{review_gate_name} status check created.")
        else:
            print(f"Failed to create {review_gate_name} status check. Response: {status_response
