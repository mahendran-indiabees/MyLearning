GitHub Enterprise Server (GHES) Migration Documentation
1. Introduction
This document outlines the process for migrating repositories from one organization (org) to another within the same GitHub Enterprise Server (GHES) instance. The migration is automated using GitHub Actions and leverages the GitHub CLI to transfer repositories. The goal is to ensure a seamless and accurate migration of repositories, including their metadata, while minimizing downtime and data loss.

2. Migration Mechanism
We are using the GitHub CLI repository transfer method to migrate repositories. This method is native to GitHub and ensures that repositories are moved (not copied) from the source organization to the target organization. The transfer process retains most repository metadata, including branches, tags, commits, pull requests, webhooks, secrets, and more.

3. What Can Be Migrated Using the Transfer Method?
The following repository content and metadata are migrated when using the GitHub CLI transfer method:

Repositories: The entire repository, including its history, is moved to the target organization.

Branches: All branches, including the default branch, are transferred.

Tags: All Git tags are preserved.

Commits: The full commit history is retained.

Pull Requests: All pull requests (open, closed, and merged) are migrated.

Issues: All issues (open and closed) are transferred.

Releases: GitHub releases and associated assets are migrated.

Wiki: Repository wikis are transferred.

Milestones: Issue and pull request milestones are preserved.

Labels: Custom labels for issues and pull requests are migrated.

Branch Protection Rules: Rules for protecting branches are retained.

Repository Settings: General repository settings (e.g., visibility, merge options) are transferred.

Webhooks: Webhooks configured in the source repository are transferred.

Secrets: Repository secrets (e.g., API keys, tokens) are transferred.

Deploy Keys: Deploy keys are transferred.

Services: GitHub services (e.g., integrations) are transferred.

Stars and Watchers: Stars and watchers associated with the repository are transferred.

4. What Cannot Be Migrated Using the Transfer Method?
The following items are not migrated during the transfer process and must be manually reconfigured in the target organization:

Collaborator Permissions: Collaborator permissions are not transferred. You must re-add collaborators to the target repository.

Repository Traffic Data: Traffic data (e.g., views, clones) is not migrated.

Forks: Repository forks are not migrated. Users must re-fork the repository from the target organization.

5. Known Considerations
Source Repository Deletion: After the transfer, the repository will no longer exist in the source organization. It will be moved to the target organization.

Repository URL Change: The repository URL will change to reflect the new organization (e.g., https://github.com/source-org/repo → https://github.com/target-org/repo).

Dependencies: Any external dependencies (e.g., CI/CD pipelines, integrations) referencing the old repository URL must be updated.

Permissions: You must have admin access to both the source and target organizations to perform the transfer.
