# data_manager\version-3.6

import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
DB_PATH = BASE_DIR / "data" / "project_manager.db"

def get_connection():
    conn = sqlite3.connect(DB_PATH)

    conn.execute("PRAGMA foreign_keys = 1")

    conn.row_factory = sqlite3.Row
    return conn

def initialize_db():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS projects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL UNIQUE,
            status TEXT NOT NULL)
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            project_id INTEGER NOT NULL,
            title TEXT NOT NULL,
            priority TEXT NOT NULL,
            due_date TEXT NOT NULL,
            created TEXT NOT NULL,
            completed INTEGER DEFAULT 0,
            FOREIGN KEY (project_id) REFERENCES projects (id) ON DELETE CASCADE
            )
    """)

    conn.commit()
    conn.close()
    print("Database Initialized Successfully. \n")

initialize_db()