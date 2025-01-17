import os
import sys

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

    for root, dirs, files in os.walk(repo_path):
        print(root)
        print(dirs)
        print(files)
        for file in files:
            for stack_name, identifiers in STACK_FILES.items():
                if file in identifiers:
                    stack.add(stack_name)
    
    return list(stack)

def main():   
    repo_path = sys.argv[1]
    print(f"Analyzing repository at: {repo_path}...")
    stack = identify_stack(repo_path)
    print("--------------------------------")
    print(stack)
    print("--------------------------------")    
    if len(stack) > 1:
        stack.insert(0, "Multiple Stacks Detected")  
    
    # Print the results
    print(f"Detected Build stack: {', '.join(stack) if stack else 'No stack detected'}")

if __name__ == "__main__":
    main()
