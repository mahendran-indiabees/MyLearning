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
    stack = set()  
    try:
        files = os.listdir(repo_path)
    except FileNotFoundError:
        print(f"Error: Directory '{repo_path}' or Files not found.")
        sys.exit(1)
    except PermissionError:
        print(f"Error: Permission denied for directory '{repo_path}'.")
        sys.exit(1)
    
    # Check only the files in the root directory
    for file in files:
        for stack_name, identifiers in STACK_FILES.items():
            if file in identifiers:
                stack.add(stack_name)
    
    return list(stack)

def main():
    # Ensure a path argument is provided
    if len(sys.argv) != 2:
        print("Usage: python script.py <repository_path>")
        sys.exit(1)
    
    repo_path = sys.argv[1]
    print(" ")
    print(f"Analyzing repository at: {repo_path}...\n")
    
    stack = identify_stack(repo_path)
    print(" ")
    print("*********************************************")
    
    if len(stack) == 0:
        print("No build stack detected.")
        sys.exit(1)
    
    if len(stack) > 1:
        print(f"Error: Multiple build stacks detected: {', '.join(stack)}")
        sys.exit(1)
    
    detected_stack = stack[0]
    print(f"Detected Build Stack: \033[1;32m{detected_stack}\033[0m") 
    print("*********************************************")

if __name__ == "__main__":
    main()
