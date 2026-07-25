# project_ops\version-3.2

import data_manager  # noqa: I001
import datetime
import ui_helpers

def get_project_selection():
    conn = data_manager.get_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM projects")
    
    projects = cursor.fetchall()
    
    if not projects:
        print("\nNo projects currently exist. Please create one first.")
        conn.close()
        return None
    
    print()
    
    for count, project in enumerate(projects, start=1):
        print(f"{count}. {project['title']}")
    print()
    
    while True:
        user_input = input("Select a Project Number (or 'q' to cancel): ")
        if user_input.lower() == 'q':
            print("\nAction Cancelled.")
            conn.close()
            return None

        try:
            user_choice = int(user_input)
            target_index = user_choice - 1

            if 0 <= target_index < len(projects):
                selected_project = projects[target_index]
                conn.close() 
                return selected_project
            else:
                print("ERROR: THAT NUMBER IS OUT OF RANGE. PLEASE TRY AGAIN.")
        except ValueError:
            print("ERROR: INVALID INPUT. PLEASE ENTER A NUMBER.")

def create_projects():
    ui_helpers.header("CREATE: A NEW PROJECT")

    while True:
        pname = input("Project Name: ").strip()
        if not pname:
            print("ERROR: PROJECT NAME CANNOT BE EMPTY. PLEASE ENTER A NAME.\n")
            continue

        conn = data_manager.get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT id FROM projects WHERE LOWER(title) = LOWER(?)", (pname,))
        existing_project = cursor.fetchone()

        if existing_project:
            print(f"ERROR: A PROJECT NAMED '{pname}' ALREADY EXISTS. PLEASE CHOOSE A DIFFERENT NAME.\n")
            continue

        break

    cursor.execute(
        "INSERT INTO projects (title, status) VALUES (?, ?)",
        (pname, "Not Started")
    )

    conn.commit()
    conn.close()

    print(f"\nProject '{pname}' created successfully.")

def edit_projects():
    ui_helpers.header("EDIT: AN EXISTING PROJECT")
    
    selected_project = get_project_selection()
    if selected_project is None:
        return
    
    print(f"\n[CURRENT] Project Title: {selected_project['title']}")
    project_id = selected_project['id']
    
    # validation loop until provided a valid name
    while True:
        new_title = input("Write a new name for the selected project: ").strip()
        
        if not new_title:
            print("ERROR: PROJECT NAME CANNOT BE EMPTY. PLEASE ENTER A NAME.\n")
            continue
            
        if new_title.lower() == selected_project['title'].lower():
            print("ERROR: THAT IS ALREADY THE CURRENT PROJECT NAME. PLEASE CHOOSE A NEW NAME.\n")
            continue
            
        # Open connection inside the loop so we can check the database for duplicates
        conn = data_manager.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT id FROM projects WHERE LOWER(title) = LOWER(?)", (new_title,))
        existing_project = cursor.fetchone()
        
        if existing_project:
            print(f"ERROR: A PROJECT NAMED '{new_title}' ALREADY EXISTS. PLEASE CHOOSE A DIFFERENT NAME.\n")
            conn.close() 
            continue
            
        break 
        
    # If the loop breaks, the name is valid. Execute the UPDATE.
    cursor.execute("UPDATE projects SET title = ? WHERE id = ?", (new_title, project_id))
    
    conn.commit()
    conn.close()
    
    print(f"\nNew Project Title '{new_title}' has successfully replaced the previous Project Title.")

def delete_projects():
    ui_helpers.header("DELETE: AN EXISTING PROJECT")
    selected_project = get_project_selection()
    
    if selected_project is None:
        return
        
    conn = data_manager.get_connection()
    cursor = conn.cursor()
    
    project_id = selected_project['id']
    project_title = selected_project['title']
    
    cursor.execute("DELETE FROM projects WHERE id = ?", (project_id,))
    
    conn.commit()
    conn.close()
    
    print(f"\nSUCCESS: Deleted '{project_title}' and all associated tasks from the database.")


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
    
    conn = data_manager.get_connection()
    cursor = conn.cursor()
    
    # Get all projects
    cursor.execute("SELECT * FROM projects")
    projects = cursor.fetchall()
    
    if not projects:
        print("No projects currently exist. Please create one first.\n")
        conn.close()
        return
        
    for project in projects:
        print("======= ============================= ========")
        print(f"Project Title: {project['title']}")
        print(f"Project Status: {project['status']}")
        print("======= ============================= ========")
        
        # Grab all tasks linked to this specific project_id
        cursor.execute("SELECT * FROM tasks WHERE project_id = ?", (project['id'],))
        tasks = cursor.fetchall()
        
        if not tasks:
            print(" -> [No tasks assigned to this project yet]")
        else:
            for count, task in enumerate(tasks, start=1):
                # SQLite stores Booleans as 1 (True) or 0 (False)
                checkbox = "[X]" if task['completed'] == 1 else "[ ]"
                print(f" {count}. {checkbox} Task: {task['title']}")
                print(f"    Priority: {task['priority']} | Created: {task['created']} | Due: {task['due_date']}")
                print()
        print()
        
    conn.close()

def change_status():
    ui_helpers.header("EDIT: THE STATUS OF A PROJECT")

    selected_project = get_project_selection()
    if selected_project is None:
        return
    
    print()
    print(f"Project Title: {selected_project['title']}")
    print("================//=================")
    print(f"Current Status: {selected_project['status']}")
    print("================//=================")
    print()
    
    ui_helpers.status_menu()

    while True:
        new_status_input = input("Enter a new status for the project: ")
        if new_status_input == "1":
            new_status = "In Progress"
            break
        elif new_status_input == "2":
            new_status = "Completed"
            break
        else:
            print("INCORRECT STATUS CHANGE OPTION!")
            
    
    conn = data_manager.get_connection()
    cursor = conn.cursor()
    
    cursor.execute(
        "UPDATE projects SET status = ? WHERE id = ?", 
        (new_status, selected_project['id'])
    )
    
    conn.commit()
    conn.close()
    
    print("\nProject status updated successfully.")

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