import sys
import json
import os
from datetime import datetime

FILE_NAME = "tasks.json"

# --- 1. Helper Functions (File Access) ---
def load_tasks():
    """Reads the JSON file. Returns an empty list if it doesn't exist."""
    if not os.path.exists(FILE_NAME):
        return []
    with open(FILE_NAME, 'r') as file:
        try:
            return json.load(file) # Converts JSON text into a Python list of dictionaries
        except json.JSONDecodeError: 
            return [] # Failsafe in case the file is empty or corrupted

def save_tasks(tasks):
    """Takes a list of dictionaries and saves it as JSON."""
    with open(FILE_NAME, 'w') as file:
        # indent=4 makes the JSON file readable for humans, not just a single long line
        json.dump(tasks, file, indent=4) 

# --- 2. Core Features ---
def add_task(description):
    tasks = load_tasks()
    
    # Logic to auto-generate an ID. If list is empty, start at 1. 
    # Otherwise, find the highest existing ID and add 1.
    new_id = 1 if not tasks else max(task['id'] for task in tasks) + 1
    
    # Get current time for timestamps
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Construct the task dictionary
    new_task = {
        "id": new_id,
        "description": description,
        "status": "todo",
        "createdAt": current_time,
        "updatedAt": current_time
    }
    
    tasks.append(new_task)
    save_tasks(tasks)
    print(f"Task added successfully (ID: {new_id})")

# --- 3. The Router (Handling sys.argv) ---
def main():
    # If they just type 'python task_cli.py' with no commands, tell them how to use it.
    if len(sys.argv) < 2:
        print("Usage: python task_cli.py <command> [arguments]")
        return

    # Grab the command and make it lowercase so "ADD" or "add" both work
    command = sys.argv[1].lower()

    if command == "add":
        # They need to provide a description. e.g., python task_cli.py add "My task"
        if len(sys.argv) < 3:
            print("Error: Please provide a task description.")
            return
        description = sys.argv[2]
        add_task(description)
        
    else:
        print(f"Unknown command: {command}")

if __name__ == "__main__":
    main()