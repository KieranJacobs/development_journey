# data_manager\version-6.4

import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "data" / "project_manager.db"

ALLOWED_TABLES = {"projects", "tasks", "attachments"}
ALLOWED_MIGRATION_COLUMNS = {
    "projects": {"description", "color"},
    "tasks": {"description", "assignee_id", "status"},
    "attachments": set(),
}


def _apply_secure_pragmas(conn):
    pragma_settings = [
        ("foreign_keys", "ON"),
        ("journal_mode", "WAL"),
        ("synchronous", "FULL"),
        ("temp_store", "MEMORY"),
        ("busy_timeout", 5000),
    ]
    for pragma_name, value in pragma_settings:
        try:
            conn.execute(f"PRAGMA {pragma_name} = {value}")
        except sqlite3.DatabaseError:
            continue

    try:
        conn.execute("PRAGMA trusted_schema = OFF")
    except sqlite3.DatabaseError:
        pass


def get_connection():
    conn = sqlite3.connect(str(DB_PATH))
    _apply_secure_pragmas(conn)
    conn.row_factory = sqlite3.Row
    return conn


def get_all_projects(search_query=None):
    conn = get_connection()
    if search_query:
        search_pattern = f"%{search_query.strip()}%"
        projects = conn.execute("SELECT * FROM projects WHERE title LIKE ?", (search_pattern,)).fetchall()
    else:
        projects = conn.execute("SELECT * FROM projects").fetchall()
    conn.close()
    return projects


def get_project_by_id(project_id):
    conn = get_connection()
    project = conn.execute("SELECT * FROM projects WHERE id = ?", (project_id,)).fetchone()
    conn.close()
    return project


def get_tasks_for_project(project_id, sort_by=None):
    conn = get_connection()
    if sort_by == 'priority':
        query = """
            SELECT * FROM tasks WHERE project_id = ?
            ORDER BY
            CASE priority
                WHEN 'High' THEN 1
                WHEN 'Moderate' THEN 2
                WHEN 'Low' THEN 3
                ELSE 4
            END ASC
        """
        tasks = conn.execute(query, (project_id,)).fetchall()
    elif sort_by == 'date':
        query = "SELECT * FROM tasks WHERE project_id = ? ORDER BY due_date ASC"
        tasks = conn.execute(query, (project_id,)).fetchall()
    else:
        tasks = conn.execute("SELECT * FROM tasks WHERE project_id = ? ORDER BY id ASC", (project_id,)).fetchall()
    conn.close()
    return tasks


def update_project_status(project_id, new_status):
    conn = get_connection()
    conn.execute(
        "UPDATE projects SET status = ? WHERE id = ?",
        (new_status, project_id)
    )
    conn.commit()
    conn.close()


def add_attachment_record(project_id, file_name, file_path):
    conn = get_connection()
    conn.execute(
        "INSERT INTO attachments (project_id, file_name, file_path) VALUES (?, ?, ?)",
        (project_id, file_name, file_path)
    )
    conn.commit()
    conn.close()


def get_attachments_for_project(project_id):
    conn = get_connection()
    attachments = conn.execute(
        "SELECT * FROM attachments WHERE project_id = ?",
        (project_id,)
    ).fetchall()
    conn.close()
    return attachments


def get_attachment_by_id(attachment_id):
    conn = get_connection()
    attachment = conn.execute(
        "SELECT * FROM attachments WHERE id = ?",
        (attachment_id,)
    ).fetchone()
    conn.close()
    return attachment


def initialize_db():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS projects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL UNIQUE,
            status TEXT NOT NULL,
            description TEXT DEFAULT '',
            color TEXT DEFAULT '#7c6af7'
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            project_id INTEGER NOT NULL,
            title TEXT NOT NULL,
            description TEXT DEFAULT '',
            assignee_id TEXT DEFAULT 'm1',
            priority TEXT NOT NULL,
            due_date TEXT NOT NULL,
            created TEXT NOT NULL,
            completed INTEGER DEFAULT 0,
            status TEXT DEFAULT 'backlog',
            FOREIGN KEY (project_id) REFERENCES projects (id) ON DELETE CASCADE
            )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS attachments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            project_id INTEGER NOT NULL,
            file_name TEXT NOT NULL,
            file_path TEXT NOT NULL,
            uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (project_id) REFERENCES projects (id) ON DELETE CASCADE
            )
        """)

    migrations = [
        ("projects", "description", "TEXT DEFAULT ''"),
        ("projects", "color", "TEXT DEFAULT '#7c6af7'"),
        ("tasks", "description", "TEXT DEFAULT ''"),
        ("tasks", "assignee_id", "TEXT DEFAULT 'm1'"),
        ("tasks", "status", "TEXT DEFAULT 'backlog'")
    ]

    for table, column, col_type in migrations:
        if table not in ALLOWED_TABLES or column not in ALLOWED_MIGRATION_COLUMNS.get(table, set()):
            continue
        try:
            cursor.execute(f"ALTER TABLE {table} ADD COLUMN {column} {col_type}")
        except sqlite3.OperationalError:
            pass

    conn.commit()
    conn.close()
    print("Database Initialized Successfully. \n")


initialize_db()