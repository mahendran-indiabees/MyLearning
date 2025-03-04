import requests
import json
import os

# Bitbucket credentials and repository details
BITBUCKET_URL = "https://bitbucket.example.com"
PROJECT_KEY = "YOUR_PROJECT_KEY"
REPO_SLUG = "YOUR_REPO_SLUG"
USERNAME = "YOUR_USERNAME"
PASSWORD = "YOUR_PASSWORD"

# Path to the backup file
BACKUP_FILE = "artifacts/branch_permissions_backup_<timestamp>.json"  # Replace <timestamp> with the actual backup file name

# Bitbucket API endpoints
RESTRICTIONS_ENDPOINT = f"{BITBUCKET_URL}/rest/branch-permissions/2.0/projects/{PROJECT_KEY}/repos/{REPO_SLUG}/restrictions"

# Headers for API requests
HEADERS = {
    "Content-Type": "application/json"
}

# Authenticate with Bitbucket
AUTH = (USERNAME, PASSWORD)

def delete_existing_restrictions():
    """Delete all existing branch restrictions."""
    restrictions = get_existing_restrictions()
    if restrictions:
        restriction_ids = [r["id"] for r in restrictions["values"]]
        for restriction_id in restriction_ids:
            delete_url = f"{RESTRICTIONS_ENDPOINT}/{restriction_id}"
            response = requests.delete(delete_url, headers=HEADERS, auth=AUTH)
            if response.status_code == 204:
                print(f"Deleted restriction with ID: {restriction_id}")
            else:
                print(f"Failed to delete restriction. Status code: {response.status_code}, Response: {response.text}")

def get_existing_restrictions():
    """Fetch existing branch restrictions from the repository."""
    response = requests.get(RESTRICTIONS_ENDPOINT, headers=HEADERS, auth=AUTH)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to fetch restrictions. Status code: {response.status_code}, Response: {response.text}")
        return None

def restore_restrictions(backup_file):
    """Restore branch restrictions from the backup file."""
    if not os.path.exists(backup_file):
        print(f"Backup file not found: {backup_file}")
        return

    with open(backup_file, "r") as f:
        restrictions = json.load(f)

    for restriction in restrictions["values"]:
        payload = {
            "type": restriction["type"]["id"],
            "matcher": restriction["matcher"],
            "users": restriction.get("users", []),
            "groups": restriction.get("groups", [])
        }
        response = requests.post(RESTRICTIONS_ENDPOINT, headers=HEADERS, auth=AUTH, data=json.dumps(payload))
        if response.status_code == 201:
            print(f"Restored restriction: {restriction['id']}")
        else:
            print(f"Failed to restore restriction. Status code: {response.status_code}, Response: {response.text}")

def main():
    # Step 1: Delete existing restrictions
    delete_existing_restrictions()

    # Step 2: Restore restrictions from backup
    restore_restrictions(BACKUP_FILE)

if __name__ == "__main__":
    main()
