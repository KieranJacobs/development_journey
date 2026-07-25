# project_ops\version-2.4

import data_manager  # noqa: I001
import datetime
import ui_helpers

def get_project_selection():
    if not data_manager.projects_list:
        print("\nNo projects currently exist. Please create one first.")
        return None
    print()
    for count, project in enumerate(data_manager.projects_list, start=1):
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

            if 0 <= target_index < len(data_manager.projects_list):
                return data_manager.projects_list[target_index]
            else:
                print("ERROR: THAT NUMBER IS OUT OF RANGE. PLEASE TRY AGAIN.")
        except ValueError:
            print("ERROR: INVALID INPUT. PLEASE ENTER A NUMBER")

def create_projects():
    data_manager.load_projects()
    ui_helpers.header("CREATE: A NEW PROJECT")
    while True:
        pname = input("Project Name?: ").strip()
        if not pname:
            print("ERROR: PROJECT NAME CANNOT BE EMPTY. PLEASE ENTER A NAME.")
            continue
        is_duplicate = any(project['title'].lower() == pname.lower() for project in data_manager.projects_list)
        if is_duplicate:
            print(f"ERROR: A PROJECT NAMED '{pname}' ALREADY EXISTS. PLEASE CHOOSE A DIFFERENT NAME.\n")
            continue
        break
    new_project = {
        "title": pname,
        "tasks": [],
        "status": "Not Started"
    }
    data_manager.projects_list.append(new_project)
    print(f"\nProject '{pname}' created successfully.")
    data_manager.save_projects()

def edit_projects():
    data_manager.load_projects()
    ui_helpers.header("EDIT: AN EXISTING PROJECT")
    selected_project = get_project_selection()
    if selected_project is None:
        return
    
    print(f"\n[CURRENT] Project Title: {selected_project['title']}")
    while True:
        new_title = input("Write a new name for the selected project: ").strip()
        if not new_title:
            print("ERROR: PROJECT NAME CANNOT BE EMPTY. PLEASE ENTER A NAME. \n")
            continue
        if new_title.lower() == selected_project['title'].lower():
            print("ERROR: THAT IS ALREADY THE CURRENT PROJECT NAME. PLEASE CHOOSE A DIFFERENT NAME.\n")
            continue
        is_duplicate = any(project['title'].lower() == new_title.lower() for project in data_manager.projects_list)
        if is_duplicate:
            print(f"ERROR: A PROJECT NAMED '{new_title}' ALREADY EXISTS. PLEASE CHOOSE A DIFFERENT PROJECT NAME. \n")
            continue
        break
    selected_project["title"] = new_title
    print(f"\nNew Project Title '{new_title}' has successfully replaced the previous Project Title.")
    data_manager.save_projects()

def delete_projects():
    data_manager.load_projects()
    ui_helpers.header("DELETE: AN EXISTING PROJECT")
    selected_project = get_project_selection()
    if selected_project is None:
        return
    data_manager.projects_list.remove(selected_project)
    print(f"\nSUCCESS: Deleted '{selected_project['title']}' from list.")
    data_manager.save_projects()


def add_task():
    data_manager.load_projects()
    ui_helpers.header("ADD: A NEW TASK TO A PROJECT")
    selected_project = get_project_selection()
    if selected_project is None:
        return
    
    print(f"\n[CURRENT] Project Selected: {selected_project['title']}")
    new_task = input("Write a basic task for the selected project: ")
    ui_helpers.priority_menu()
    while True:
        new_priority = input("Select a Priority level for this task(1,2,3): ")
        if new_priority == "1":
            prio = "High"
            break
        elif new_priority == "2":
            prio = "Moderate"
            break
        elif new_priority == "3":
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
        "title": new_task,
        "priority": prio,
        "completed": False,
        "created": formatted_time,
        "due date": string_date
    }

    selected_project["tasks"].append(task)
    print(f"\nTask '{new_task}' has been successfully added to Project '{selected_project['title']}'")
    data_manager.save_projects()

def view_projects():
    ui_helpers.header("VIEW: ALL EXISTING PROJECTS")
    data_manager.load_projects()
    if not data_manager.projects_list:
        print("No projects currently exist. Please create one first. \n")
        return
    for project in data_manager.projects_list:
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
    ui_helpers.header("EDIT: THE STATUS OF A PROJECT")
    data_manager.load_projects()

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
    ui_helpers.status_menu()

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
    data_manager.save_projects()

def toggle_task_completion():
    data_manager.load_projects()
    ui_helpers.header("TOGGLE: TASK COMPLETION")

    selected_project = get_project_selection()
    if selected_project is None:
        return

    tasks = selected_project.get("tasks", [])
    if not tasks:
        print(f"    -> [No tasks assigned to '{selected_project['title']}' yet]\n")
        return

    print(f"\nTasks for '{selected_project['title']}':")
    for count, task in enumerate(tasks, start=1):
        checkbox = "[X]" if task.get("completed") else "[ ]"
        print(f" {count}. {checkbox} {task['title']}")
    print()

    while True:
        user_input = input("Select a Task Number to toggle (or 'q' to cancel): ")
        if user_input.lower() == 'q':
            print("\nAction Cancelled.")
            return

        try:
            task_index = int(user_input) - 1
            if 0 <= task_index < len(tasks):
                selected_task = tasks[task_index]

                selected_task["completed"] = not selected_task.get("completed", False)
                status_text = "Completed" if selected_task["completed"] else "Incomplete"

                print(f"\n SUCCESS: Task '{selected_task['title']}' marked as {status_text}.")
                data_manager.save_projects()
                break
            else:
                print("ERROR: THAT NUMBER IS OUT OF RANGE. PLEASE TRY AGAIN.")
        except ValueError:
            print("ERROR: INVALID INPUT. PLEASE ENTER A NUMBER.")

def delete_task():
    data_manager.load_projects()
    ui_helpers.header("DELETE: A TASK")

    selected_project = get_project_selection()
    if selected_project is None:
        return
    tasks = selected_project.get("tasks", [])
    if not tasks:
        print(f"    -> [No tasks assigned to '{selected_project['title']}' yet]\n")
        return

    print(f"\nTasks for '{selected_project['title']}':")
    for count, task in enumerate(tasks, start=1):
        print(f"    {count}, {task['title']}")
    print()

    while True:
        user_input = input("Select a Task Number to delete (or 'q' to cancel): ")
        if user_input.lower() == 'q':
            print("\nAction Cancelled.")
            return

        try:
            task_index = int(user_input) - 1
            if 0 <= task_index < len(tasks):
                deleted_task = tasks.pop(task_index)
                print(f"\nSUCCESS: Deleted task '{deleted_task['title']}' from project '{selected_project['title']}'.")
                data_manager.save_projects()
                break
            else:
                print("ERROR: THAT NUMBER IS OUT OF RANGE. PLEASE TRY AGAIN.")
        except ValueError:
            print("ERROR: INVALID INPUT. PLEASE ENTER A NUMBER.")