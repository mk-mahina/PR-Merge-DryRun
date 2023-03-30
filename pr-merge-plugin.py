import os
from github import Github

# get the authentication token from environment variable
token = os.environ['GITHUB_TOKEN']

# create a Github object
g = Github(token)

# get the repository object
repo = g.get_repo('mk-mahina/PR-Merge-DryRun')

# get all open pull requests in the repository
pulls = repo.get_pulls(state='open')

# loop through each pull request
for pr in pulls:
    print(f"Checking pull request #{pr.number}...")
    
    # check if the pull request is approved
    if pr.get_reviews().totalCount > 0 and all(review.state == 'APPROVED' for review in pr.get_reviews()):
        print("Pull request approved, waiting for manual approval...")

        print(pr.assignee.login)

        pr.remove_from_assignees(pr.assignee.login)

        # assign the pull request to a user for manual approval
        pr.add_to_assignees("armin-mahina")

        pr.update()  # update the pr object with the new assignee

        print(pr.assignee.login)

        # Create a comment on the pull request
        pr.create_issue_comment(f'This pull request is waiting for manual approval from @{pr.assignee.login} before merging.')

        # wait for manual approval
        print(f"Pull request assigned to @{pr.assignee.login}, waiting for approval...")
        while pr.get_reviews().totalCount == 0 or not all(review.state == 'APPROVED' for review in pr.get_reviews()):
            pr.update()
        
       
    else:
        print(f"Pull request #{pr.number} is not approved, skipping...")
