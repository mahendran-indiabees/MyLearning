#!/bin/bash

ORG="your-source-org"  # Replace with your source organization name

# List all repositories in the organization
REPOS=$(gh repo list $ORG --json nameWithOwner --jq '.[].nameWithOwner')

# Iterate through each repository
for REPO in $REPOS; do
  # Check if .gitattributes file exists
  if gh api repos/$REPO/contents/.gitattributes --silent > /dev/null 2>&1; then
    echo "Git LFS is used in repository: $REPO"
  fi
done
