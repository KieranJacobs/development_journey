# main.py\version-2.0\

import json
from pathlib import Path
import datetime

SAVE_FILE = Path("projects/projects_list.json")
projects_list = []

def menu_function():
    print()
    print("====== //                         // ======")
    print("====== / PROJECT MANAGEMENT SYSTEM / ======")
    print("         1. Create a Project               ")
    print("         2. Add a Task                     ")
    print("         3. Change Project Name/Title      ")
    print("         4. Change Project Status          ")
    print("         5. Delete a Project               ")
    print("         6. View all Projects              ")
    print("         7. Close Program                  ")
    print("====== //                         // ======")
    print()

def create_projects():
    load_projects()
    print("====== //                         // ======")
    print("====== /   CREATE: A NEW PROJECT   / ======")
    print("====== //                         // ======")
    pname = input("Project Name?: ").strip()
    new_project = {
        "title": pname,
        "tasks": [],
        "status": "Not Started"
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

def edit_projects():
    load_projects()
    print()
    print("====== //                         // ======")
    print("====== /   EDIT: A PROJECTS TITLE  / ======")
    print("====== //                         // ======")
    selectProject = input("Input a Project to edit: ")
    found = False
    for project in projects_list:
        if project['title'] == selectProject:
            found = True
            print(f"[CURRENT] Project Title: {project['title']}.")
            new_Title = input("Write a new name for Selected project: ")
            newTitle = {"title": new_Title}
            project["title"] = newTitle
            print(f"\nNew Project Title '{new_Title}' has successfully replaced previous Title.")
            save_projects()
    if not found:
        print("INVALID PROJECT TITLE!\n")

def delete_projects():
    load_projects()
    print()
    print("====== //                         // ======")
    print("====== /     DELETE: A PROJECT     / ======")
    print("====== //                         // ======")
    print()
    for count, project in enumerate(projects_list, start=1):
        print()
        print(f"{count}. Project Title: {project.get('title')}")
        print()
    selectProject = input("Select a Project Number to delete: ")
    try:
        user_choice = int(selectProject)
        target_index = user_choice - 1

        if 0 <= target_index < len(projects_list):
            deleted_project = projects_list.pop(target_index)
            print(f"\nSuccess: Deleted '{deleted_project.get('title', 'Unknown')}' from list.")

            save_projects()
        else:
            print("\nERROR: THAT NUMBER IS OUT OF RANGE. PLEASE SELECT A VALID MENU NUMBER!")
    except ValueError:
        print("\nERROR: INVALID INPUT. PLEASE ENTER A NUMBER.")

def add_task():
    load_projects()
    print()
    print("====== //                         // ======")
    print("= / SELECT: A PROJECT TO ADD A TASK FOR / =")
    print("====== //                         // ======")
    selectProject = input("Project Title: ")
    found = False
    for project in projects_list:
        if project["title"].strip().lower() == selectProject.strip().lower():
            found = True
            new_Task = input("Write a basic task for the selected project: ")
            print("===================================")
            print("====== // PRIORITY LEVELS // ======")
            print("===================================")
            print("1. High")
            print("2. Moderate")
            print("3. Low")
            print()
            while True:
                new_prio = input("Select a Priority level for this task(1,2,3): ")
                if new_prio == "1":
                    prio = "High"
                    break
                elif new_prio == "2":
                    prio = "Moderate"
                    break
                elif new_prio == "3":
                    prio = "Low"
                    break
                else:
                    print("INVALID PRIORITY LEVEL SELECTED!")
                
            while True:
                try:
                    due_date = input("Enter the deadline for this task (DD-MM-YYYY): ")
                    parsed_date = datetime.datetime.strptime(due_date, "%d-%m-%Y")
                    string_date = parsed_date.strftime("%d-%m-%Y")
                    break
                except ValueError:
                    print("\nERROR: INVALID FORMAT! PLEASE USE DD-MM-YYYY!")

            raw_time = datetime.datetime.now()
            formatted_time = raw_time.strftime("%d-%m-%Y")

            task = {
                "title": new_Task,
                "priority": prio,
                "completed": False,
                "created": formatted_time,
                "due date": string_date
            }
            project["tasks"].append(task)
            print(f"\nTask '{new_Task}' has been successfully added to Project.")
            save_projects()
            break
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
            tasks = project["tasks"]
            count = 0
            print(f"Title: {project['title']}")
            for task in tasks:
                count += 1
                print(f"{count}. Task: {task['title']}")
            
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
        edit_projects()
    
    elif user_input == "4":
        change_status()

    elif user_input == "5":
        delete_projects()
    
    elif user_input == "6":
        view_projects()
    
    elif user_input == "7":
        break

    else:
        print()
        print("INVALID OPTION CHOSEN!")
        print()