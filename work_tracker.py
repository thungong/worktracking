import streamlit as st
import pandas as pd
import os
from datetime import datetime

# Streamlit app configuration
st.set_page_config(page_icon="✅", page_title="Work Tracker - V2.42")

# Sidebar title
st.sidebar.title("✅ Work Tracker - V2.42")

# Define the paths for CSV files
CSV_FILE = "tasks.csv"
ARCHIVE_FILE = "archive.csv"

# Function to load tasks from CSV
def load_tasks():
    if os.path.exists(CSV_FILE) and os.path.getsize(CSV_FILE) > 0:
        df = pd.read_csv(CSV_FILE)
        # Ensure that all required columns are present
        required_columns = ['Task', 'Description', 'Category', 'Priority', 'Start Time', 'End Time', 'Total Time (hours:minutes)', 'Status']
        for col in required_columns:
            if col not in df.columns:
                df[col] = None
        df.fillna("Not Set", inplace=True)  # Replace NaN with "Not Set"
        return df
    else:
        return pd.DataFrame(columns=required_columns)

# Function to save tasks to CSV
def save_tasks():
    st.session_state['tasks'].to_csv(CSV_FILE, index=False)

# Function to add a new task
def add_task():
    new_task = pd.DataFrame({
        'Task': [st.session_state['task_name']],
        'Description': [st.session_state['description'] if st.session_state['description'] else "Not Set"],
        'Category': [st.session_state['category']],
        'Priority': [st.session_state['priority']],
        'Start Time': [None],
        'End Time': [None],
        'Total Time (hours:minutes)': [None],
        'Status': ['Not Started']
    })
    st.session_state['tasks'] = pd.concat([st.session_state['tasks'], new_task], ignore_index=True)
    save_tasks()  # Save tasks after adding
    st.experimental_rerun()  # Clear form fields by reloading the page

# Function to start timing a task
def start_task(task_index):
    current_time = pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S")  # Convert timestamp to string
    st.session_state['tasks'].at[task_index, 'Start Time'] = current_time
    st.session_state['tasks'].at[task_index, 'End Time'] = None  # Reset end time when starting
    st.session_state['tasks'].at[task_index, 'Status'] = 'Active'
    save_tasks()  # Save tasks after starting
    st.experimental_rerun()  # Rerun to reflect changes immediately

# Function to stop timing a task and mark as completed
def stop_task(task_index):
    current_time = pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S")  # Convert timestamp to string
    start_time = st.session_state['tasks'].at[task_index, 'Start Time']
    if pd.notnull(start_time):
        st.session_state['tasks'].at[task_index, 'End Time'] = current_time
        total_time_seconds = (pd.Timestamp(current_time) - pd.to_datetime(start_time)).total_seconds()
        hours, remainder = divmod(total_time_seconds, 3600)
        minutes, _ = divmod(remainder, 60)
        st.session_state['tasks'].at[task_index, 'Total Time (hours:minutes)'] = f"{int(hours)}:{int(minutes)}"
        st.session_state['tasks'].at[task_index, 'Status'] = 'Completed'
        save_tasks()  # Save tasks after stopping
        st.experimental_rerun()  # Rerun to reflect changes immediately

# Function to archive a task and remove it from tasks.csv
def archive_task(task_index):
    # Load archive file
    if os.path.exists(ARCHIVE_FILE):
        archive_df = pd.read_csv(ARCHIVE_FILE)
    else:
        archive_df = pd.DataFrame(columns=st.session_state['tasks'].columns)

    # Add the completed task to the archive
    archive_df = pd.concat([archive_df, st.session_state['tasks'].iloc[[task_index]]], ignore_index=True)

    # Save to archive.csv
    archive_df.to_csv(ARCHIVE_FILE, index=False)

    # Remove the completed task from the current tasks
    st.session_state['tasks'] = st.session_state['tasks'].drop(index=task_index).reset_index(drop=True)
    save_tasks()
    st.experimental_rerun()

# Load tasks into session state
if 'tasks' not in st.session_state:
    st.session_state['tasks'] = load_tasks()

# Show input form
task_name = st.sidebar.text_input("Task Name", key="task_name")
description = st.sidebar.text_area("Task Description", key="description")
category = st.sidebar.selectbox("Category", ["Administration", "Project", "Support-App", "Support-Other", "Development", "Meetings", "Research", "Other"], key="category")
priority = st.sidebar.selectbox("Priority", ["Low", "Medium", "High"], key="priority")

# Sidebar for adding a new task at the bottom
if st.sidebar.button("Add Task"):
    if st.session_state.get("task_name", ""):
        add_task()
    else:
        st.sidebar.warning("Please enter a task name.")

# Display tasks in a card-like format
st.header("Your Tasks")
if not st.session_state['tasks'].empty:
    for i, row in st.session_state['tasks'].iterrows():
        start_time_display = row['Start Time'] if pd.notnull(row['Start Time']) and row['Start Time'] != 'Not Set' else 'Not Started'
        end_time_display = str(row['End Time']) if pd.notnull(row['End Time']) and row['End Time'] != 'Not Set' else ''
        card_color = "#fff" if row['Status'] != "Active" else "#d3e2ff"

        st.markdown(f"""
            <div class="card" style="background-color: {card_color};">
                <h4>Task {i+1}: {row['Task']} ({row['Priority']} Priority)</h4>
                <p><strong>Category:</strong> {row['Category']}</p>
                <p><strong>Description:</strong> {row['Description']}</p>
                <p><strong>Start Time:</strong> {start_time_display}</p>
                {f'<p><strong>End Time:</strong> {end_time_display}</p>' if end_time_display else ''}
            </div>
        """, unsafe_allow_html=True)

        # Show buttons for Completed tasks
        if row['Status'] == 'Completed':
            if st.button(f"Restart Task {i+1}", key=f"restart_{i}"):
                start_task(i)
            if st.button(f"Archive Task {i+1}", key=f"archive_{i}"):
                archive_task(i)
        # Show buttons for Active or Not Started tasks
        else:
            if pd.isnull(row['Start Time']) or row['Start Time'] == 'Not Set':
                if st.button(f"Start Task {i+1}", key=f"start_{i}"):
                    start_task(i)
            else:
                if st.button(f"Stop Task {i+1}", key=f"stop_{i}"):
                    stop_task(i)

# Editable Summary table
st.header("Summary")
if not st.session_state['tasks'].empty:
    edited_df = st.data_editor(st.session_state['tasks'], num_rows="dynamic", key="summary_editor")
    if edited_df is not None:
        st.session_state['tasks'] = edited_df
        save_tasks()

# Custom CSS for styling the cards and buttons
st.markdown(
    """
    <style>
    .stApp {
        background-color: #c0c9d9;
    }
    .card {
        background-color: #ffffff;
        border-radius: 10px;
        padding: 15px;
        margin: 15px 0;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
    }
    .card h4 {
        margin: 0;
        font-size: 18px;
        color: #333333;
    }
    .card p {
        margin: 5px 0;
        color: #555555;
    }
    .btn {
        border: none;
        border-radius: 5px;
        padding: 10px 20px;
        font-size: 16px;
        cursor: pointer;
        margin-right: 5px;
    }
    .btn-start {
        background-color: #4CAF50;
        color: white;
    }
    .btn-start:hover {
        background-color: #45a049;
    }
    .btn-stop {
        background-color: #f44336;
        color: white;
    }
    .btn-stop:hover {
        background-color: #da190b;
    }
    </style>
    """,
    unsafe_allow_html=True
)
