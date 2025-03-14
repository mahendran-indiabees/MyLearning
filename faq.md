FAQ: Repository Migration from Bitbucket to GitHub Enterprise
This document addresses common questions and considerations for users migrating repositories from Bitbucket Self-Hosted Data Center to GitHub Enterprise Instance (Self-Hosted). Please review the following information to understand the changes and customizations required during the migration process.

1. Branch Permissions Migration
Q: How are branch permissions migrated from Bitbucket to GitHub?
A: Branch permissions in Bitbucket are partially migrated to GitHub. However, some configurations, such as Default Reviewers, will not be migrated. Users will need to manually configure certain settings in GitHub after migration.

Q: What happens to the "Prevent Rewriting History" option in Bitbucket?
A:

Bitbucket Setting: "Prevent Rewriting History"

GitHub Equivalent: "Allow Force Pushes"

By default, all protected branches in GitHub have "Allow Force Pushes" disabled. If you need to allow force pushes for specific users or branches, you must:

Enable "Allow Force Pushes" for the branch.

Use Rulesets to configure exemptions (e.g., block force pushes for specific users or branches).

Q: What happens to the "Prevent Deletion" option in Bitbucket?
A:

Bitbucket Setting: "Prevent Deletion"

GitHub Equivalent: "Allow Deletions"

By default, all protected branches in GitHub have "Allow Deletions" disabled. If you need to allow branch deletions for specific users or branches, you must:

Enable "Allow Deletions" for the branch.

Use Rulesets to configure exemptions (e.g., restrict deletions for specific users or branches).

Q: What happens to the "Prevent All Changes (Read-Only)" option in Bitbucket?
A:

Bitbucket Setting: "Prevent All Changes (Read-Only)"

GitHub Equivalent: "Lock Branch" or "Restrict Updates"

After migration, you must manually enable the "Lock Branch" option in GitHub to restrict changes. If you need to allow updates for specific users or branches, you can use Rulesets to configure exemptions (e.g., restrict updates for specific users or branches).

2. Default Reviewers
Q: Are Default Reviewers migrated from Bitbucket to GitHub?
A: No, Default Reviewers configurations in Bitbucket are not migrated to GitHub. After migration, you will need to manually configure default reviewers in GitHub using CODEOWNERS files or GitHub's Protected Branch Rules.

3. Customization After Migration
Q: What customizations are required after migration?
A: After migrating repositories from Bitbucket to GitHub, users must manually configure the following:

Branch Protection Rules: Adjust settings like "Allow Force Pushes," "Allow Deletions," and "Lock Branch" as needed.

Rulesets: Use GitHub Rulesets to enforce specific policies for branches, such as blocking force pushes or restricting deletions.

Default Reviewers: Set up default reviewers using CODEOWNERS or GitHub's protected branch settings.
