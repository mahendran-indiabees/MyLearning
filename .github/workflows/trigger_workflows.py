import os
import time
import requests

# Constants
MAX_RUNNING_WORKFLOWS = 15  # Number of available runners for child workflows
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")  # Provide via GitHub Secrets
GITHUB_REPO = os.getenv("GITHUB_REPOSITORY")  # e.g., "owner/repo"
CHILD_WORKFLOW_ID = "child-workflow.yml"  # Name of the child workflow file
REPO_LIST = os.getenv("REPO_LIST").split()
RESULT_FILE = "migration_results.txt"

# Initialize variables
running_workflows = []
completed_results = []

# Helper function to trigger child workflow
def trigger_workflow(repo_name):
    url = f"https://api.github.com/repos/{GITHUB_REPO}/actions/workflows/{CHILD_WORKFLOW_ID}/dispatches"
    headers = {
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }
    payload = {"ref": "main", "inputs": {"repo_name": repo_name}}
    response = requests.post(url, headers=headers, json=payload)

    if response.status_code == 204:
        print(f"Triggered workflow for repo: {repo_name}")
        return True
    else:
        print(f"Failed to trigger workflow for {repo_name}: {response.json()}")
        return False

# Helper function to check workflow status
def check_workflow_status(workflow_id):
    url = f"https://api.github.com/repos/{GITHUB_REPO}/actions/runs/{workflow_id}"
    headers = {
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        status = response.json().get("status")
        conclusion = response.json().get("conclusion")
        return status, conclusion
    else:
        print(f"Failed to fetch status for workflow {workflow_id}: {response.json()}")
        return None, None

# Main execution loop
for repo in REPO_LIST:
    # Wait until a runner becomes available
    while len(running_workflows) >= MAX_RUNNING_WORKFLOWS:
        print("Max workflows running. Checking for available runners...")
        for workflow in running_workflows[:]:
            status, conclusion = check_workflow_status(workflow["id"])
            if status == "completed":
                print(f"Workflow for {workflow['repo']} completed with status: {conclusion}")
                completed_results.append(f"ChildJob-{workflow['repo']}: {conclusion}")
                running_workflows.remove(workflow)
        time.sleep(10)  # Poll every 10 seconds

    # Trigger new workflow
    if trigger_workflow(repo):
        workflow_id = {"id": repo, "repo": repo}  # Replace with actual workflow ID logic
        running_workflows.append(workflow_id)

# Wait for all workflows to complete
print("Waiting for all workflows to finish...")
while running_workflows:
    for workflow in running_workflows[:]:
        status, conclusion = check_workflow_status(workflow["id"])
        if status == "completed":
            print(f"Workflow for {workflow['repo']} completed with status: {conclusion}")
            completed_results.append(f"ChildJob-{workflow['repo']}: {conclusion}")
            running_workflows.remove(workflow)
    time.sleep(10)

# Write results to a file
with open(RESULT_FILE, "w") as f:
    f.write("\n".join(completed_results))

print("Migration completed. Results saved to", RESULT_FILE)
