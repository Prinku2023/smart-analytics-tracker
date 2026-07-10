import streamlit as st
import tracker_engine as engine
import database_setup as setup

setup.init_tracker_db()

# Page configurations
st.set_page_config(page_title="Project Analytics Tracker", layout="wide")
st.title("📊 Smart Project Analytics Dashboard")
st.markdown("Track project progress, map tasks, and analyze development delivery metrics in real-time.")

# --- SIDEBAR: ADD PROJECTS & SETTINGS ---
with st.sidebar:
    st.header("📂 Project Management")
    
    # Form to insert a new project
    with st.form("new_project_form", clear_on_submit=True):
        new_project_name = st.text_input("New Project Name", placeholder="e.g., E-Commerce Portal")
        new_project_desc = st.text_area("Description", placeholder="Project goals and stack details...")
        submit_project = st.form_submit_button("Create Project")
        
        if submit_project:
            if new_project_name.strip():
                success = engine.add_project(new_project_name, new_project_desc)
                if success:
                    st.success(f"Project '{new_project_name}' created!")
                    st.rerun()
                else:
                    st.error("A project with this name already exists.")
            else:
                st.error("Project name cannot be empty.")

    st.markdown("---")
    st.markdown("💡 **Tip:** Deleting a project will automatically cascade and delete all associated tasks in the relational database.")

# --- MAIN SCREEN LAYOUT ---
projects = engine.get_all_projects()

if not projects:
    st.info("No projects found! Create your first project in the sidebar to get started.")
else:
    # 1. Project Selector Dropdown
    project_list = {p["name"]: p["project_id"] for p in projects}
    selected_project_name = st.selectbox("Select Project to Analyze", list(project_list.keys()))
    selected_project_id = project_list[selected_project_name]
    
    # Get current project description
    current_proj = next(p for p in projects if p["project_id"] == selected_project_id)
    st.caption(f"📝 *Description: {current_proj['description'] or 'No description provided.'}*")
    
    # Fetch tasks for the chosen project
    tasks = engine.get_tasks_for_project(selected_project_id)
    
    # 2. CALCULATE METRICS (Analytics Engine)
    total_tasks = len(tasks)
    completed_tasks = sum(1 for t in tasks if t["status"] == "Completed")
    pending_tasks = total_tasks - completed_tasks
    
    # Progress Calculation
    progress_percent = (completed_tasks / total_tasks) if total_tasks > 0 else 0.0
    
    # High Priority task count
    high_priority_pending = sum(1 for t in tasks if t["priority"] == "High" and t["status"] == "Pending")
    
    # Display Analytic Cards
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric(label="Total Tasks", value=total_tasks)
    with col2:
        st.metric(label="Completed Tasks", value=f"{completed_tasks} / {total_tasks}")
    with col3:
        st.metric(label="Completion Rate", value=f"{progress_percent * 100:.1f}%")
    with col4:
        st.metric(label="⚠️ Critical Pending Tasks", value=high_priority_pending, delta_color="inverse")
        
    # Visual Progress Bar
    st.progress(progress_percent)
    
    st.markdown("### Task Matrix")
    
    # 3. TASK CREATION INTERFACE
    with st.expander("➕ Add New Task to this Project", expanded=False):
        with st.form("new_task_form", clear_on_submit=True):
            t_col1, t_col2, t_col3 = st.columns([3, 1, 1])
            with t_col1:
                task_title = st.text_input("Task Title", placeholder="e.g., Integrate payment gateway API")
            with t_col2:
                task_priority = st.selectbox("Priority Level", ["Low", "Medium", "High"])
            with t_col3:
                task_eta = st.number_input("ETA (Days)", min_value=1, max_value=90, value=3)
                
            submit_task = st.form_submit_button("Add Task to Ledger")
            if submit_task:
                if task_title.strip():
                    engine.add_task(selected_project_id, task_title, task_priority, task_eta)
                    st.success("Task appended to project!")
                    st.rerun()
                else:
                    st.error("Task title cannot be blank.")
                    
    # 4. TASK INTERACTIVE TABLE
    if total_tasks == 0:
        st.info("No tasks recorded for this project yet. Use the expander panel above to populate some tasks!")
    else:
        # Display each task with an interactive toggle button
        for task in tasks:
            t_id = task["task_id"]
            t_title = task["title"]
            t_priority = task["priority"]
            t_status = task["status"]
            t_eta = task["eta_days"]
            
            # Styling badges based on status and priority
            p_badge = "🔴 High" if t_priority == "High" else ("🟡 Medium" if t_priority == "Medium" else "🟢 Low")
            status_text = "✅ Completed" if t_status == "Completed" else "⏳ Pending"
            
            # Render a neat control row for each task
            row_col1, row_col2, row_col3, row_col4 = st.columns([4, 1.5, 1.5, 1.5])
            with row_col1:
                # Strike-through completed tasks visually
                if t_status == "Completed":
                    st.markdown(f"~~{t_title}~~")
                else:
                    st.markdown(f"**{t_title}**")
            with row_col2:
                st.markdown(f"Priority: {p_badge}")
            with row_col3:
                st.markdown(f"ETA: **{t_eta} Days**")
            with row_col4:
                # Clickable checkbox toggle button that calls our python database update function!
                button_label = "Mark Pending" if t_status == "Completed" else "Mark Done"
                if st.button(button_label, key=f"toggle_{t_id}"):
                    engine.toggle_task_status(t_id, t_status)
                    st.rerun()
            st.divider()

    # 5. DANGER ZONE: DELETE PROJECT
    st.markdown("### ⚠️ Danger Zone")
    if st.button("🗑️ Delete Current Project Permanently"):
        engine.delete_project(selected_project_id)
        st.success(f"Project '{selected_project_name}' removed.")
        st.rerun()
