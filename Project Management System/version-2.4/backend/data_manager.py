# data_manager\version-2.3

import json
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
SAVE_FILE = BASE_DIR / "projects" / "projects_list.json"

projects_list = []

def save_projects():
    SAVE_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(SAVE_FILE, "w") as file:
        json.dump(projects_list, file, indent=4)
        print("JSON file successfully saved.")
        print()

def load_projects():
    global projects_list
    if SAVE_FILE.exists():
        with open(SAVE_FILE, "r") as file:
            projects_list = json.load(file)
            print("JSON file successfully loaded.")
            print()
    
    if not SAVE_FILE.exists():
        print("PATH DOES NOT EXIST, CHECK IF JSON FILE HAS BEEN GENERATED!")
        print()