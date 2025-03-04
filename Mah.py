
Below is a **Python script** that automates the process of creating read-only restrictions in Bitbucket using the REST API. This script can be integrated into a **GitHub Actions workflow** to achieve the desired flow.

---

### **Python Script: Bitbucket Read-Only Restrictions Automation**

```python
import requests
import json
import os
from datetime import datetime

# Bitbucket credentials and repository details
BITBUCKET_URL = "https://bitbucket.example.com"
PROJECT_KEY = "YOUR_PROJECT_KEY"
REPO_SLUG = "YOUR_REPO_SLUG"
USERNAME = "YOUR_USERNAME"
PASSWORD = "YOUR_PASSWORD"

# GitHub Actions artifact path
ARTIFACT_DIR = "artifacts"
BACKUP_FILE = f"{ARTIFACT_DIR}/branch_permissions_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"

# Bitbucket API endpoints
RESTRICTIONS_ENDPOINT = f"{BITBUCKET_URL}/rest/branch-permissions/2.0/projects/{PROJECT_KEY}/repos/{REPO_SLUG}/restrictions"

# Headers for API requests
HEADERS = {
    "Content-Type": "application/json"
}

# Authenticate with Bitbucket
AUTH = (USERNAME, PASSWORD)

def get_existing_restrictions():
    """Fetch existing branch restrictions from the repository."""
    response = requests.get(RESTRICTIONS_ENDPOINT, headers=HEADERS, auth=AUTH)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to fetch restrictions. Status code: {response.status_code}, Response: {response.text}")
        return None

def create_read_only_restriction():
    """Create a read-only restriction for all branches."""
    payload = {
        "type": "read-only",
        "matcher": {
            "id": "**",
            "displayId": "**",
            "type": {
                "id": "PATTERN",
                "name": "Pattern"
            }
        }
    }
    response = requests.post(RESTRICTIONS_ENDPOINT, headers=HEADERS, auth=AUTH, data=json.dumps(payload))
    if response.status_code == 201:
        print("Read-only restriction created successfully.")
    else:
        print(f"Failed to create restriction. Status code: {response.status_code}, Response: {response.text}")

def delete_restrictions(restriction_ids):
    """Delete existing restrictions."""
    for restriction_id in restriction_ids:
        delete_url = f"{RESTRICTIONS_ENDPOINT}/{restriction_id}"
        response = requests.delete(delete_url, headers=HEADERS, auth=AUTH)
        if response.status_code == 204:
            print(f"Deleted restriction with ID: {restriction_id}")
        else:
            print(f"Failed to delete restriction. Status code: {response.status_code}, Response: {response.text}")

def save_backup(restrictions):
    """Save existing restrictions to a backup file."""
    if not os.path.exists(ARTIFACT_DIR):
        os.makedirs(ARTIFACT_DIR)
    with open(BACKUP_FILE, "w") as f:
        json.dump(restrictions, f, indent=4)
    print(f"Backup saved to {BACKUP_FILE}")

def main():
    # Step 1: Check if any restrictions exist
    restrictions = get_existing_restrictions()
    if restrictions:
        print("Existing restrictions found.")
        # Step 2: Save backup of current restrictions
        save_backup(restrictions)
        # Step 3: Delete existing restrictions
        restriction_ids = [r["id"] for r in restrictions["values"]]
        delete_restrictions(restriction_ids)
    else:
        print("No existing restrictions found.")

    # Step 4: Create read-only restrictions
    create_read_only_restriction()

if __name__ == "__main__":
    main()
```

---

### **GitHub Actions Workflow**

Below is an example GitHub Actions workflow to run the Python script:

```yaml
name: Bitbucket Read-Only Restrictions Automation

on:
  workflow_dispatch:

jobs:
  automate-bitbucket-restrictions:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout repository
        uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: "3.9"

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install requests

      - name: Run Python script
        env:
          BITBUCKET_URL: ${{ secrets.BITBUCKET_URL }}
          PROJECT_KEY: ${{ secrets.PROJECT_KEY }}
          REPO_SLUG: ${{ secrets.REPO_SLUG }}
          USERNAME: ${{ secrets.BITBUCKET_USERNAME }}
          PASSWORD: ${{ secrets.BITBUCKET_PASSWORD }}
        run: |
          python bitbucket_restrictions.py

      - name: Upload backup as artifact
        uses: actions/upload-artifact@v3
        with:
          name: branch-permissions-backup
          path: artifacts/
```

---

### **Explanation of the Flow**

1. **Check Existing Restrictions:**
   - The script fetches existing branch restrictions using the Bitbucket REST API.

2. **Backup Existing Restrictions:**
   - If restrictions exist, they are saved to a backup file (`branch_permissions_backup_<timestamp>.json`).

3. **Delete Existing Restrictions:**
   - The script deletes all existing restrictions to ensure a clean slate.

4. **Create Read-Only Restrictions:**
   - A new read-only restriction is created for all branches (`**`).

5. **Upload Backup to GitHub Artifacts:**
   - The backup file is uploaded as a GitHub Actions artifact for future use.

6. **Rollback (Manual Process):**
   - If migration fails, you can manually restore the restrictions using the backup file.

---

### **How to Use**

1. Replace the placeholders (`YOUR_PROJECT_KEY`, `YOUR_REPO_SLUG`, etc.) in the script with your actual Bitbucket details.
2. Add the required secrets (`BITBUCKET_URL`, `PROJECT_KEY`, `REPO_SLUG`, `BITBUCKET_USERNAME`, `BITBUCKET_PASSWORD`) to your GitHub repository's secrets.
3. Push the script and workflow to your repository.
4. Trigger the workflow manually or configure it to run on specific events.

---

### **Rollback Process**

To restore the original restrictions:
1. Download the backup artifact from the GitHub Actions run.
2. Use the Bitbucket REST API to reapply the restrictions from the backup file.

Let me know if you need further assistance!
