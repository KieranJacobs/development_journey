# main.py\version-2.2\

import datetime
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
    print("         3. Change Project Name/Title      ")
    print("         4. Change Project Status          ")
    print("         5. Delete a Project               ")
    print("         6. View all Projects              ")
    print("         7. Close Program                  ")
    print("====== //                         // ======")
    print()

def get_project_selection():
    if not projects_list:
        print("\nNo projects currently exist. Please create one first.")
        return None
    print()
    for count, project in enumerate(projects_list, start=1):
        print(f"{count}. {project.get('title')}")
    print()
    while True:
        user_input = input("Select a Project Number (or 'q' to cancel): ")
        if user_input.lower() == 'q':
            print("\nAction Cancelled.")
            return None

        try:
            user_choice = int(user_input)
            target_index = user_choice - 1

            if 0 <= target_index < len(projects_list):
                return projects_list[target_index]
            else:
                print("ERROR: THAT NUMBER IS OUT OF RANGE. PLEASE TRY AGAIN.")
        except ValueError:
            print("ERROR: INVALID INPUT. PLEASE ENTER A NUMBER")

def create_projects():
    load_projects()
    print("====== //                         // ======")
    print("====== /   CREATE: A NEW PROJECT   / ======")
    print("====== //                         // ======")

    while True:
        pname = input("Project Name?: ").strip()

        if not pname:
            print("ERROR: PROJECT NAME CANNOT BE EMPTY. PLEASE ENTER A NAME.")
            continue

        is_duplicate = any(project['title'].lower() == pname.lower() for project in projects_list)

        if is_duplicate:
            print(f"ERROR: A PROJECT NAMED '{pname}' ALREADY EXISTS. PLEASE CHOOSE A DIFFERENT NAME.\n")
            continue
        break

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
    selected_project = get_project_selection()

    if selected_project is None:
        return
    
    print(f"\n[CURRENT] Project Title: {selected_project['title']}")
    new_Title = input("Write a new name for the selected project: ").strip()
    selected_project["title"] = new_Title

    print(f"\nNew Project Title '{new_Title}' has successfully replaced the previous Project Title.")
    save_projects()

def delete_projects():
    load_projects()
    print()
    print("====== //                         // ======")
    print("====== /     DELETE: A PROJECT     / ======")
    print("====== //                         // ======")
    print()
    selected_project = get_project_selection()

    if selected_project is None:
        return

    projects_list.remove(selected_project)

    print(f"\nSUCCESS: Deleted '{selected_project['title']}' from list.")
    save_projects()


def add_task():
    load_projects()
    print()
    print("====== //                         // ======")
    print("= / SELECT: A PROJECT TO ADD A TASK FOR / =")
    print("====== //                         // ======")
    selected_project = get_project_selection()
    if selected_project is None:
        return
    
    print(f"\n[CURRENT] Project Selected: {selected_project['title']}")
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
            parsed_date = datetime.datetime.strptime(due_date, "%d-%m-%Y").replace(tzinfo=datetime.timezone.utc)
            string_date = parsed_date.strftime("%d-%m-%Y")
            break
        except ValueError:
            print("\nERROR: INVALID FORMAT! PLEASE USE DD-MM-YYYY!")

    raw_time = datetime.datetime.now(datetime.timezone.utc)
    formatted_time = raw_time.strftime("%d-%m-%Y")

    task = {
        "title": new_Task,
        "priority": prio,
        "completed": False,
        "created": formatted_time,
        "due date": string_date
    }

    selected_project["tasks"].append(task)
    print(f"\nTask '{new_Task}' has been successfully added to Project '{selected_project["title"]}'")
    save_projects()

def view_projects():
    print()
    print("====== //                         // ======")
    print("===== / VIEW: ALL EXISTING PROJECTS / =====")
    print("====== //                         // ======")
    print()
    load_projects()

    if not projects_list:
        print("No projects currently exist. Please create one first. \n")
        return

    for project in projects_list:
        print("======= ============================= ========")
        print(f"Project Title: {project['title']}")
        print(f"Project Status: {project['status']}")
        print("======= ============================= ========")

        tasks = project["tasks"]

        if not tasks:
            print(" -> [No tasks assigned to this project yet]")
        else:
            for count, task in enumerate(tasks, start=1):
                checkbox = "[X]" if task.get("completed") else "[ ]"
                print(f" {count}. {checkbox} Task: {task['title']}")

                priority = task.get('priority', 'Unknown')
                created = task.get('created', 'Unknown')
                due = task.get('due date', 'Unknown')

                print(f"    Priority: {priority} | Created: {created} | Due: {due}")
                print()
        print()

def change_status():
    print()
    print("======= //                         // ========")
    print("======= / CHANGE: A PROJECTS STATUS / ========")
    print("======= //                         // ========")
    print()

    load_projects()

    selected_project = get_project_selection()

    if selected_project is None:
        return
    
    print()
    print(f"Project Title: {selected_project['title']}")
    print("================//=================")
    print(f"Current Status: {selected_project['status']}")
    print("================//=================")
    print()
    print()
    print("Possible Statuses: ")
    print("1. In Progress")
    print("2. Completed")
    print()

    while True:
        new_status = input("Enter a new status for the project: ")
        if new_status == "1":
            selected_project["status"] = "In Progress"
            break
        elif new_status == "2":
            selected_project["status"] = "Completed"
            break
        else:
            print("INCORRECT STATUS CHANGE OPTION!")
    
    print("\nProject status updated successfully.")
    save_projects()



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