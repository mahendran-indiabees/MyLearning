#!/bin/bash

# Constants
MAX_RUNNING_WORKFLOWS=15 # Number of available runners for child workflows
GITHUB_TOKEN="${GITHUB_TOKEN}" # Provide via environment variable
GITHUB_REPO="${GITHUB_REPOSITORY}" # e.g., "owner/repo"
CHILD_WORKFLOW_ID="child-workflow.yml" # Name of the child workflow file
REPO_LIST=(${REPO_LIST}) # List of repositories to process
RESULT_FILE="migration_results.txt"

# Variables
declare -a running_workflows
declare -a completed_results

# Helper function to trigger child workflow
trigger_workflow() {
    local repo_name="$1"
    local url="https://api.github.com/repos/${GITHUB_REPO}/actions/workflows/${CHILD_WORKFLOW_ID}/dispatches"
    local payload="{\"ref\":\"main\",\"inputs\":{\"repo_name\":\"${repo_name}\"}}"

    response=$(curl -s -o /dev/null -w "%{http_code}" -X POST \
        -H "Authorization: Bearer ${GITHUB_TOKEN}" \
        -H "Accept: application/vnd.github.v3+json" \
        -d "$payload" "$url")

    if [[ "$response" == "204" ]]; then
        echo "Triggered workflow for repo: ${repo_name}"
        return 0
    else
        echo "Failed to trigger workflow for ${repo_name}. HTTP Status: $response"
        return 1
    fi
}

# Helper function to check workflow status
check_workflow_status() {
    local workflow_id="$1"
    local url="https://api.github.com/repos/${GITHUB_REPO}/actions/runs/${workflow_id}"
    local response=$(curl -s -H "Authorization: Bearer ${GITHUB_TOKEN}" \
        -H "Accept: application/vnd.github.v3+json" "$url")

    local status=$(echo "$response" | jq -r ".status")
    local conclusion=$(echo "$response" | jq -r ".conclusion")
    echo "$status|$conclusion"
}

# Main execution loop
for repo in "${REPO_LIST[@]}"; do
    # Wait until a runner becomes available
    while [[ ${#running_workflows[@]} -ge $MAX_RUNNING_WORKFLOWS ]]; do
        echo "Max workflows running. Checking for available runners..."
        for i in "${!running_workflows[@]}"; do
            workflow_info=(${running_workflows[$i]})
            workflow_id=${workflow_info[0]}
            repo_name=${workflow_info[1]}
            status_conclusion=$(check_workflow_status "$workflow_id")
            status=$(echo "$status_conclusion" | cut -d '|' -f 1)
            conclusion=$(echo "$status_conclusion" | cut -d '|' -f 2)

            if [[ "$status" == "completed" ]]; then
                echo "Workflow for ${repo_name} completed with status: $conclusion"
                completed_results+=("ChildJob-${repo_name}: $conclusion")
                unset 'running_workflows[$i]'
            fi
        done
        sleep 10
    done

    # Trigger new workflow
    if trigger_workflow "$repo"; then
        # NOTE: Replace this with actual logic to fetch workflow ID
        workflow_id="dummy-workflow-id-${repo}"
        running_workflows+=("${workflow_id} ${repo}")
    fi
done

# Wait for all workflows to complete
echo "Waiting for all workflows to finish..."
while [[ ${#running_workflows[@]} -gt 0 ]]; do
    for i in "${!running_workflows[@]}"; do
        workflow_info=(${running_workflows[$i]})
        workflow_id=${workflow_info[0]}
        repo_name=${workflow_info[1]}
        status_conclusion=$(check_workflow_status "$workflow_id")
        status=$(echo "$status_conclusion" | cut -d '|' -f 1)
        conclusion=$(echo "$status_conclusion" | cut -d '|' -f 2)

        if [[ "$status" == "completed" ]]; then
            echo "Workflow for ${repo_name} completed with status: $conclusion"
            completed_results+=("ChildJob-${repo_name}: $conclusion")
            unset 'running_workflows[$i]'
        fi
    done
    sleep 10
done

# Write results to a file
echo "${completed_results[@]}" | tr ' ' '\n' > "$RESULT_FILE"
echo "Migration completed. Results saved to $RESULT_FILE"
