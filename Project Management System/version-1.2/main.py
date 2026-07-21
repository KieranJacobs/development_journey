# main.py\version-1.2\

import json
from pathlib import Path

SAVE_FILE = Path("projects/projects_list.json")
projects_list = []

def menu_function():
    print()
    print("====== //                         // ======")
    print("====== / PROJECT MANAGEMENT SYSTEM / ======")
    print("         1. Create a Project               ")
    print("         2. Add a Task                     ")
    print("         3. Save a Project to JSON         ")
    print("         4. Load a Project from JSON       ")
    print("         5. Change Project Status          ")
    print("         6. View all Projects              ")
    print("         7. Close Program                  ")
    print("====== //                         // ======")
    print()

def create_projects():
    print("====== //                         // ======")
    print("====== /   CREATE: A NEW PROJECT   / ======")
    print("====== //                         // ======")
    pname = input("Project Name?: ").strip()

    new_project = {
        "title": pname,
        "tasks": [],
        "status": "Not Started",
        "completed": False
    }

    projects_list.append(new_project)
    print(f"\nProject '{pname}' created successfully.")
    save_projects()

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

def add_task():
    print()
    print("====== //                         // ======")
    print("= / SELECT: A PROJECT TO ADD A TASK FOR / =")
    print("====== //                         // ======")
    selectProject = input("Project Title: ")
    found = False
    for project in projects_list:
        if project["title"] == selectProject:
            found = True
            new_Task = input("Write a basic task for the selected project: ")
            
            task = {
                "title": new_Task
            }

            project["tasks"].append(task)
            print(f"\nTask '{new_Task}' has been successfully added to Project.")
            save_projects()
        if not found:
            print("INVALID PROJECT TITLE!\n")

def view_projects():
    print()
    print("====== //                         // ======")
    print("===== / VIEW: ALL EXISTING PROJECTS / =====")
    print("====== //                         // ======")
    print()
    with SAVE_FILE.open("r") as file:
        projects = json.load(file)
        for project in projects:
            print(f"Title: {project['title']}")
            print(f"Tasks: {project['tasks']}")
            print(f"Status?: {project['status']}")
            print()

def change_status():
    print()
    print("======= //                         // ========")
    print("======= / CHANGE: A PROJECTS STATUS / ========")
    print("======= //                         // ========")
    print()
    load_projects()
    selectProject = input("Enter a Project title: ")
    found = False
    for project in projects_list:
        if project['title'] == selectProject:
            found = True

            print()
            print(f"Project Title: {project['title']}")
            print("================//=================")
            print(f"Current Status: {project['status']}")
            print("================//=================")
            print()

            print("Possible Statuses: ")
            print("1. In Progress")
            print("2. Completed")
            print()

            new_status = input("Enter a new status for the project: ")
            if new_status == "1":
                project["status"] = "In Progress"
                print("Project status updated successfully.")
                print()

            elif new_status == "2":
                project["status"] = "Completed"
                print("Project status updated successfully.")
                print()

            else:
                print("INCORRECT STATUS CHANGE OPTION!")
                print()
            save_projects()
            break

    if not found:
        print("INVALID PROJECT TITLE!")
        print()



while True:
    menu_function()
    user_input = input("Please Select a Number from the Menu: ")
    
    if user_input == "1":
        create_projects()
    
    elif user_input == "2":
        add_task()

    elif user_input == "3":
        save_projects()
    
    elif user_input == "4":
        load_projects()

    elif user_input == "5":
        change_status()
    
    elif user_input == "6":
        view_projects()
    
    elif user_input == "7":
        break

    else:
        print()
        print("INVALID OPTION CHOSEN!")
        print()