import sqlite3
import time

def get_db_connection():
    """Establishes a connection to the tracker database with row-factory enabled."""
    conn = sqlite3.connect("tracker.db")
    conn.row_factory = sqlite3.Row  # Allows us to access columns by name like dictionary keys
    return conn

# --- CREATE OPERATIONS ---
def add_project(name, description):
    """Inserts a new project into the relational database."""
    conn = get_db_connection()
    cursor = conn.cursor()
    created_date = time.strftime('%Y-%m-%d')
    try:
        cursor.execute(
            "INSERT INTO projects (name, description, created_date) VALUES (?, ?, ?)",
            (name, description, created_date)
        )
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False  # Project name already exists
    finally:
        conn.close()

def add_task(project_id, title, priority, eta_days):
    """Inserts a task mapped to a parent project_id."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO tasks (project_id, title, priority, status, eta_days) VALUES (?, ?, ?, 'Pending', ?)",
        (project_id, title, priority, eta_days)
    )
    conn.commit()
    conn.close()

# --- READ OPERATIONS ---
def get_all_projects():
    """Retrieves all rows from the projects table."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM projects")
    rows = cursor.fetchall()
    conn.close()
    return rows

def get_tasks_for_project(project_id):
    """Retrieves all tasks associated with a specific project id."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tasks WHERE project_id = ?", (project_id,))
    rows = cursor.fetchall()
    conn.close()
    return rows

# --- UPDATE OPERATIONS ---
def toggle_task_status(task_id, current_status):
    """Swaps task status between Pending and Completed."""
    new_status = "Completed" if current_status == "Pending" else "Pending"
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE tasks SET status = ? WHERE task_id = ?", (new_status, task_id))
    conn.commit()
    conn.close()

# --- DELETE OPERATIONS ---
def delete_project(project_id):
    """Removes a project and cascades down to remove all its associated tasks."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("PRAGMA foreign_keys = ON") # Enforce cascade constraints
    cursor.execute("DELETE FROM projects WHERE project_id = ?", (project_id,))
    conn.commit()
    conn.close()