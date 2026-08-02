# project_ops\version-4.2

from backend import data_manager
import datetime


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

def delete_task_web(task_id):
    conn = data_manager.get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    conn.commit()
    conn.close()
    return "SUCCESS"

def get_statistics_web():
    conn = data_manager.get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM projects")
    total_projects = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*), SUM(CASE WHEN completed = 1 THEN 1 ELSE 0 END) FROM tasks")
    task_row = cursor.fetchone()
    total_tasks = task_row[0] or 0
    completed_tasks = task_row[1] or 0
    pending_tasks = total_tasks - completed_tasks
    conn.close()
    return {
        "total_projects": total_projects,
        "total_tasks": total_tasks,
        "completed_tasks": completed_tasks,
        "pending_tasks": pending_tasks
    }

def get_export_data_web():
    conn = data_manager.get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT p.title, t.title, t.completed
        FROM projects p
        LEFT JOIN tasks t ON p.id = t.project_id
    """)
    rows = cursor.fetchall()
    conn.close()
    return rows