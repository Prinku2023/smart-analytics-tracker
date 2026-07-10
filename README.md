# 📊 Smart Project Analytics Dashboard

A responsive, full-stack Project Analytics and Task Tracking system engineered in Python. The application implements a relational database structure with multi-entity mappings (Projects and Tasks) and compiles real-time delivery telemetry on an interactive web dashboard.

## 🚀 Live Demo & Repository Links
* **Live Web Application:** [View Live App](https://smart-analytics-tracker.streamlit.app/) *(Will work once we deploy!)*
* **GitHub Repository:** [Source Code](https://github.com/Prinku2023/smart-analytics-tracker)

---

## 🏛️ System Architecture

The application is built using a modern decoupled three-tier software architecture:

```text
  [Streamlit Frontend UI] <--- (SQL Queries) ---> [Python CRUD Engine]
                                                        |
                                            (Foreign Key Constraints)
                                                        |
                                                        v
                                                 [SQLite DB File]
                                    
Presentation Layer (app.py): An interactive web panel built using Streamlit that processes user inputs, displays progress states, and renders metric cards dynamically.

Logic Engine (tracker_engine.py): A custom database middleware layer that executes safe Parameterized SQL queries to manage CRUD (Create, Read, Update, Delete) transactions.

Storage Layer (tracker.db): A persistent, local SQLite relational database storing normalized structured tables linked via cascading foreign keys.

⚡ Key Features & Engineering Practices
Relational Database Schema: Designed structured tables mapping a One-to-Many (1 to N) relationship from Projects to Tasks.

Database Referential Integrity: Implemented explicit SQLite foreign keys with ON DELETE CASCADE constraints, ensuring that deleting a project automatically cleans up and deletes all its child tasks, preventing orphaned rows.

State Interactivity: Integrated active status toggle routines that query the database to alter task states (Pending <-> Completed), instantly recalculating project completion percentages.

SQL Injection Protection: Enforced strict parameterized queries across all dynamic database transactions to sanitize inputs and prevent database security vulnerabilities.

🛠️ Tech Stack Used
Language: Python 3

Framework: Streamlit (Web UI)

Database Engine: SQLite3 (Relational Storage)

Data Manipulation: Pandas (Query Dataframe parsing)