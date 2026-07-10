import sqlite3

def init_tracker_db():
    conn = sqlite3.connect("tracker.db")
    cursor = conn.cursor()
    
    # 1. Create Projects Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS projects (
            project_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            description TEXT,
            created_date TEXT NOT NULL
        )
    """)
    
    # 2. Create Tasks Table (Linked to Projects via Foreign Key)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            task_id INTEGER PRIMARY KEY AUTOINCREMENT,
            project_id INTEGER,
            title TEXT NOT NULL,
            priority TEXT CHECK(priority IN ('Low', 'Medium', 'High')),
            status TEXT CHECK(status IN ('Pending', 'Completed')),
            eta_days INTEGER,
            FOREIGN KEY(project_id) REFERENCES projects(project_id) ON DELETE CASCADE
        )
    """)
    
    # Insert some starter projects if the table is empty
    cursor.execute("SELECT COUNT(*) FROM projects")
    if cursor.fetchone()[0] == 0:
        import time
        current_time = time.strftime('%Y-%m-%d')
        cursor.execute("INSERT INTO projects (name, description, created_date) VALUES (?, ?, ?)", 
                       ("FinTech App Development", "Building core banking modules", current_time))
        cursor.execute("INSERT INTO projects (name, description, created_date) VALUES (?, ?, ?)", 
                       ("AI Model Evaluation", "Testing LLM parameters locally", current_time))
        
    conn.commit()
    conn.close()
    print("🚀 Relational Database tracker.db initialized with seed data successfully!")

if __name__ == "__main__":
    init_tracker_db()