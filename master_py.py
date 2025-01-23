import requests
import time
from math import ceil

# GitHub API token (stored as an environment variable or replace with your token)
GITHUB_TOKEN = "your_github_token"
# GitHub organization or user
GITHUB_ORG = "your_org"
# Master repository containing the master workflow
MASTER_REPO = "master-repo"
# Workflow file name in the child repositories
WORKFLOW_FILE = "child-workflow.yml"
# Total self-hosted runners
RUNNER_CAPACITY = 25
# Number of workflows per batch
WORKFLOWS_PER_BATCH = 5

# Headers for GitHub API requests
HEADERS = {
    "Authorization": f"Bearer {GITHUB_TOKEN}",
    "Accept": "application/vnd.github+json",
}

# List of repositories to process (replace with your list of repositories)
REPOS = [f"repo-{i}" for i in range(1, 101)]


def trigger_workflow(repo_name, ref="main", inputs=None, labels=None):
    """
    Trigger a GitHub Actions workflow dispatch event.

    :param repo_name: Name of the repository
    :param ref: Branch or tag to run the workflow on
    :param inputs: Dictionary of workflow inputs
    :param labels: Runner labels for targeted execution
    """
    url = f"https://api.github.com/repos/{GITHUB_ORG}/{repo_name}/actions/workflows/{WORKFLOW_FILE}/dispatches"
    data = {
        "ref": ref,
        "inputs": inputs or {},
    }
    if labels:
        data["inputs"]["runner_labels"] = labels

    response = requests.post(url, headers=HEADERS, json=data)
    if response.status_code == 204:
        print(f"Workflow triggered for {repo_name} on {ref}.")
    else:
        print(
            f"Failed to trigger workflow for {repo_name}: {response.status_code} {response.text}"
        )


def batch_process_repositories(repos, workflows_per_batch, max_capacity):
    """
    Orchestrate workflows in batches.

    :param repos: List of repositories
    :param workflows_per_batch: Number of workflows to trigger per batch
    :param max_capacity: Maximum number of concurrent workflows
    """
    total_batches = ceil(len(repos) / workflows_per_batch)
    print(f"Total repositories: {len(repos)}, Total batches: {total_batches}")

    for batch_index in range(total_batches):
        batch_start = batch_index * workflows_per_batch
        batch_end = batch_start + workflows_per_batch
        current_batch = repos[batch_start:batch_end]

        print(f"Processing batch {batch_index + 1}/{total_batches}...")
        for repo in current_batch:
            trigger_workflow(repo_name=repo, inputs={"batch": batch_index + 1})
            time.sleep(0.5)  # Small delay to avoid hitting API rate limits

        # Wait for the batch to complete if the runner capacity is maxed out
        if (batch_index + 1) % (max_capacity // workflows_per_batch) == 0:
            print(f"Waiting for batch {batch_index + 1} to complete...")
            time.sleep(60)  # Adjust based on expected workflow completion time


if __name__ == "__main__":
    batch_process_repositories(REPOS, WORKFLOWS_PER_BATCH, RUNNER_CAPACITY)
