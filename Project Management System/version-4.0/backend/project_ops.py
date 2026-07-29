# project_ops\version-4.0

from backend import data_manager
import datetime
import csv


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

def create_project_web(title, status):
    if not title or title.strip() == "":
        return "ERROR: Project name cannot be empty."
        
    conn = data_manager.get_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT id FROM projects WHERE LOWER(title) = LOWER(?)", (title.strip(),))
    existing_project = cursor.fetchone()
    
    if existing_project:
        conn.close()
        return f"ERROR: A project named '{title}' already exists."

    cursor.execute(
        "INSERT INTO projects (title, status) VALUES (?, ?)",
        (title.strip(), status)
    )
    conn.commit()
    conn.close()
    
    return "SUCCESS"

def delete_projects():
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

def add_task_web(project_id, title, priority, due_date):
    if not title or title.strip() == "":
        return "ERROR: Task title cannot be empty."

    raw_time = datetime.datetime.now(datetime.timezone.utc)
    formatted_time = raw_time.strftime("%d-%m-%Y")

    try:
        parsed_date = datetime.datetime.strptime(due_date, "%Y-%m-%d").replace(tzinfo=datetime.timezone.utc)
        string_date = parsed_date.strftime("%d-%m-%Y")
    except ValueError:
        string_date = "No Date"

    conn = data_manager.get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO tasks (project_id, title, priority, due_date, created, completed)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (project_id, title.strip(), priority, string_date, formatted_time, 0))

    conn.commit()
    conn.close()
    return "SUCCESS"

def delete_project_web(project_id):
    conn = data_manager.get_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM projects WHERE id = ?", (project_id,))

    conn.commit()
    conn.close()

    return "SUCCESS"

def change_project_status_web(project_id, new_status):
    conn = data_manager.get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE projects SET status = ? WHERE id = ?",
        (new_status, project_id)
    )

    conn.commit()
    conn.close()

    return "SUCCESS"

def toggle_task_web(task_id):
    conn = data_manager.get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT completed FROM tasks WHERE id = ?", (task_id,))
    task = cursor.fetchone()

    if task:
        new_status = 0 if task['completed'] == 1 else 1
        cursor.execute("UPDATE tasks SET completed = ? WHERE id = ?", (new_status, task_id))
        conn.commit()

    conn.close()
    return "SUCCESS"