import os
import sys

# Define build stack identifiers
STACK_FILES = {
    "Maven": ["pom.xml"],
    "Gradle": ["build.gradle", "build.gradle.kts"],
    "Ant": ["build.xml"],
    "Python": ["requirements.txt", "setup.py", "Pipfile", "pyproject.toml"],
    "Node.js": ["package.json"],
    "Go": ["go.mod"],
    "DotNet": [".csproj", ".vbproj", ".sln"]
}

def identify_stack(repo_path):
    """Identify the stack for a repository from the local file system."""
    stack = set()

    # Walk through the directory structure
    for root, dirs, files in os.walk(repo_path):
        for file in files:
            for stack_name, identifiers in STACK_FILES.items():
                if file in identifiers:
                    stack.add(stack_name)
    
    # Convert to a list for return
    return list(stack)

def main():
    """Main function to process repositories."""
    # Get the repository path from command-line arguments
    if len(sys.argv) < 2:
        print("Usage: python my_script.py <repository_path>")
        sys.exit(1)
    
    repo_path = sys.argv[1]
    print(f"Analyzing repository at: {repo_path}...")
    
    stack = identify_stack(repo_path)
    if len(stack) > 1:
        stack.insert(0, "Multiple Stacks Detected")  # Add a warning for multiple stacks
    
    # Print the results
    print(f"Detected stack: {', '.join(stack) if stack else 'No stack detected'}")

if __name__ == "__main__":
    main()
