import os
import requests

# Get environment variables
token = os.environ['SECRET_TOKEN']
repository = "mk-mahina/PR-Merge-DryRun"
pull_number = os.environ['PULL_NUMBER']

# Set API URLs
pr_url = f"https://api.github.com/repos/{repository}/pulls/{pull_number}"
reviews_url = f"{pr_url}/reviews"

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

# Check if armin-mahina has been added as a reviewer to the pull request
reviews_response = requests.get(reviews_url, headers=headers)
reviews_data = reviews_response.json()
reviewers = [reviewer["user"]["login"] for reviewer in reviews_data]
if "armin-mahina" not in reviewers:
    reviewers_payload = {
        "reviewers": ["armin-mahina"]
    }
    reviewers_response = requests.post(reviews_url, headers=headers, json=reviewers_payload)
    if reviewers_response.ok:
        print("armin-mahina added as a reviewer to the pull request.")
    else:
        print(f"Failed to add armin-mahina as a reviewer to the pull request. Response: {reviewers_response.text}")
else:
    # Check if Armin has approved the pull request
    armin_review = next((review for review in reviews_data if review["user"]["login"] == "armin-mahina"), None)
    if armin_review is None:
        print("Armin has not reviewed the pull request yet. Exiting.")
        exit(0)
    elif armin_review["state"] != "approved":
        print("Armin has not approved the pull request yet. Exiting.")
        exit(0)
    else:
        print("Armin has approved the pull request. Proceeding with the merge.")
