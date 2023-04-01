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

# Assign the pull request to "armin-mahina" and remove existing assignees

        print(pr.assignee.login)

        pr.remove_from_assignees(pr.assignee.login)

        # assign the pull request to a user for manual approval
        pr.add_to_assignees("armin-mahina")

        pr.update()  # update the pr object with the new assignee

        print(pr.assignee.login)


