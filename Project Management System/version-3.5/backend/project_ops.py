# project_ops\version-3.5

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
    
    
    while True:
        new_title = input("Write a new name for the selected project: ").strip()
        
        if not new_title:
            print("ERROR: PROJECT NAME CANNOT BE EMPTY. PLEASE ENTER A NAME.\n")
            continue
        
        if new_title.lower() == selected_project['title'].lower():
            print("ERROR: THAT IS ALREADY THE CURRENT PROJECT NAME. PLEASE CHOOSE A NEW NAME.\n")
            continue
        
        
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
    ui_helpers.header("ADD: A NEW TASK TO A PROJECT")
    selected_project = get_project_selection()
    if selected_project is None:
        return
    
    print(f"\n[CURRENT] Project Selected: {selected_project['title']}")
    new_task = input("Write a basic task for the selected project: ")
    
    
    priority = ui_helpers.get_valid_priority()
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
    
    conn = data_manager.get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        INSERT INTO tasks (project_id, title, priority, due_date, created, completed)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (selected_project['id'], new_task, priority, string_date, formatted_time, 0))
    
    conn.commit()
    conn.close()
    print(f"\nTask '{new_task}' has been successfully added to Project '{selected_project['title']}'")

def view_projects():
    ui_helpers.header("VIEW: ALL EXISTING PROJECTS")
    
    conn = data_manager.get_connection()
    cursor = conn.cursor()
    
    
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
        
        
        cursor.execute("SELECT * FROM tasks WHERE project_id = ?", (project['id'],))
        tasks = cursor.fetchall()
        
        if not tasks:
            print(" -> [No tasks assigned to this project yet]")
        else:
            for count, task in enumerate(tasks, start=1):
                
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
    
    new_status = ui_helpers.get_valid_status()
    
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
    ui_helpers.header("TOGGLE: TASK COMPLETION")
    
    selected_project = get_project_selection()
    if selected_project is None:
        return
    
    conn = data_manager.get_connection()
    cursor = conn.cursor()
    
    
    cursor.execute("SELECT * FROM tasks WHERE project_id = ?", (selected_project['id'],))
    tasks = cursor.fetchall()
    
    if not tasks:
        print(f"  -> [No tasks assigned to '{selected_project['title']}' yet]\n")
        conn.close()
        return
    print(f"\nTasks for '{selected_project['title']}':")
    for count, task in enumerate(tasks, start=1):
        checkbox = "[X]" if task['completed'] == 1 else "[ ]"
        print(f"  {count}. {checkbox} {task['title']}")
    print()
    while True:
        user_input = input("Select a Task Number to toggle (or 'q' to cancel): ")
        if user_input.lower() == 'q':
            print("\nAction Cancelled.")
            break
        try:
            task_index = int(user_input) - 1
            if 0 <= task_index < len(tasks):
                selected_task = tasks[task_index]
                
                
                new_status = 0 if selected_task['completed'] == 1 else 1
                
                
                cursor.execute("UPDATE tasks SET completed = ? WHERE id = ?", (new_status, selected_task['id']))
                conn.commit()
                
                status_text = "Completed" if new_status == 1 else "Incomplete"
                print(f"\nSUCCESS: Task '{selected_task['title']}' marked as {status_text}.")
                break
            else:
                print("ERROR: THAT NUMBER IS OUT OF RANGE. PLEASE TRY AGAIN.")
        except ValueError:
            print("ERROR: INVALID INPUT. PLEASE ENTER A NUMBER.")
            
    conn.close()

def delete_task():
    ui_helpers.header("DELETE: A TASK")
    
    selected_project = get_project_selection()
    if selected_project is None:
        return
    
    conn = data_manager.get_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM tasks WHERE project_id = ?", (selected_project['id'],))
    tasks = cursor.fetchall()
    
    if not tasks:
        print(f"  -> [No tasks assigned to '{selected_project['title']}' yet]\n")
        conn.close()
        return
    print(f"\nTasks for '{selected_project['title']}':")
    for count, task in enumerate(tasks, start=1):
        print(f"  {count}. {task['title']}")
    print()
    while True:
        user_input = input("Select a Task Number to delete (or 'q' to cancel): ")
        if user_input.lower() == 'q':
            print("\nAction Cancelled.")
            break
        try:
            task_index = int(user_input) - 1
            if 0 <= task_index < len(tasks):
                selected_task = tasks[task_index]
                
                cursor.execute("DELETE FROM tasks WHERE id = ?", (selected_task['id'],))
                conn.commit()
                
                print(f"\nSUCCESS: Deleted task '{selected_task['title']}' from project '{selected_project['title']}'.")
                break
            else:
                print("ERROR: THAT NUMBER IS OUT OF RANGE. PLEASE TRY AGAIN.")
        except ValueError:
            print("ERROR: INVALID INPUT. PLEASE ENTER A NUMBER.")
    
    conn.close()

def project_statistics():
    ui_helpers.header("PROJECT & TASK STATISTICS")
    conn = data_manager.get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(id) FROM projects")
    total_projects = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(id) FROM tasks")
    total_tasks = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(id) FROM tasks WHERE completed = 1")
    completed_tasks = cursor.fetchone()[0]
    remaining = total_tasks - completed_tasks
    
    completion_rate = (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0
    print(f"  Total Projects:  {total_projects}")
    print(f"  Total Tasks:     {total_tasks}")
    print(f"  Tasks Completed: {completed_tasks}")
    print(f"  Tasks Remaining: {remaining}")
    print(f"  Completion Rate: {completion_rate:.0f}%")
    print()
    
    conn.close()

def search_projects():
    ui_helpers.header("SEARCH PROJECTS")
    search_term = input("Enter a partial name to search for: ").strip()
    
    if not search_term:
        print("Search cancelled.\n")
        return
    conn = data_manager.get_connection()
    cursor = conn.cursor()
    
    query_term = f"%{search_term}%" 
    
    cursor.execute("SELECT * FROM projects WHERE title LIKE ?", (query_term,))
    results = cursor.fetchall()
    
    if not results:
        print(f"\nNo projects found matching '{search_term}'.")
    else:
        print(f"\n--- Search Results for '{search_term}' ---")
        for project in results:
            print(f" - {project['title']} (Status: {project['status']})")
    
    conn.close()

def view_high_priority_tasks():
    ui_helpers.header("VIEW: HIGH PRIORITY TASKS")
    selected_project = get_project_selection()
    if selected_project is None:
        return
        
    conn = data_manager.get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT * FROM tasks 
        WHERE project_id = ? AND priority = 'High' AND completed = 0
        ORDER BY created ASC
    """, (selected_project['id'],))
    
    tasks = cursor.fetchall()
    
    if not tasks:
        print("\nNo pending High Priority tasks for this project! Great job.")
    else:
        print(f"\n--- HIGH PRIORITY TASKS FOR '{selected_project['title']}' ---")
        for count, task in enumerate(tasks, start=1):
            print(f" {count}. {task['title']} (Due: {task['due_date']})")
            
    conn.close()

def view_completed_tasks():
    ui_helpers.header("VIEW: COMPLETED TASKS")
    selected_project = get_project_selection()
    if selected_project is None:
        return
        
    conn = data_manager.get_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM tasks WHERE project_id = ? AND completed = 1", (selected_project['id'],))
    tasks = cursor.fetchall()
    
    if not tasks:
        print("\nNo completed tasks for this project yet.")
    else:
        print(f"\n--- COMPLETED TASKS FOR '{selected_project['title']}' ---")
        for count, task in enumerate(tasks, start=1):
            print(f" ✓ {task['title']}")
    
    conn.close()
