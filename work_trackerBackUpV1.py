import streamlit as st
import pandas as pd
import os

# Streamlit app configuration
st.set_page_config(page_icon="✅", page_title="Work Tracker - V1.13")

# Sidebar title
st.sidebar.title("✅ Work Tracker - V1.13")

# Define the path for the CSV file
CSV_FILE = "tasks.csv"

# Function to load tasks from CSV
def load_tasks():
    if os.path.exists(CSV_FILE) and os.path.getsize(CSV_FILE) > 0:
        return pd.read_csv(CSV_FILE)
    else:
        return pd.DataFrame(columns=['Task', 'Start Time', 'End Time', 'Total Time (minutes)'])

# Function to save tasks to CSV
def save_tasks():
    st.session_state['tasks'].to_csv(CSV_FILE, index=False)

# Function to add a new task
def add_task(task_name):
    new_task = pd.DataFrame({
        'Task': [task_name],
        'Start Time': [None],
        'End Time': [None],
        'Total Time (minutes)': [0]
    })
    st.session_state['tasks'] = pd.concat([st.session_state['tasks'], new_task], ignore_index=True)
    save_tasks()  # Save tasks after adding

# Function to start timing a task
def start_task(task_index):
    st.session_state['tasks'].at[task_index, 'Start Time'] = pd.Timestamp.now()
    st.session_state['tasks'].at[task_index, 'End Time'] = None  # Reset end time when starting
    save_tasks()  # Save tasks after starting

# Function to stop timing a task
def stop_task(task_index):
    end_time = pd.Timestamp.now()
    start_time = st.session_state['tasks'].at[task_index, 'Start Time']
    if pd.notnull(start_time):
        st.session_state['tasks'].at[task_index, 'End Time'] = end_time
        total_time_seconds = (end_time - pd.to_datetime(start_time)).total_seconds()
        st.session_state['tasks'].at[task_index, 'Total Time (minutes)'] = total_time_seconds / 60  # Convert to minutes
        st.session_state['tasks'].at[task_index, 'Start Time'] = None  # Reset start time
        save_tasks()  # Save tasks after stopping

# Load tasks into session state
if 'tasks' not in st.session_state:
    st.session_state['tasks'] = load_tasks()

# Sidebar for adding a new task
st.sidebar.header("Add a New Task")
task_name = st.sidebar.text_input("Task Name")
if st.sidebar.button("Add Task"):
    if task_name:
        add_task(task_name)
        st.sidebar.success("Task added successfully!", icon="✅")
    else:
        st.sidebar.warning("Please enter a task name.")

# Display tasks in a table-like format
st.header("Your Tasks")
if not st.session_state['tasks'].empty:
    for i, row in st.session_state['tasks'].iterrows():
        st.write(f"**Task {i+1}: {row['Task']}**")
        
        # Start Task Button
        if pd.isnull(row['Start Time']):
            if st.button(f"Start Task {i+1}", key=f"start_{i}"):
                start_task(i)
                st.experimental_rerun()  # Rerun the script to reflect changes immediately
        
        # Stop Task Button
        else:
            if st.button(f"Stop Task {i+1}", key=f"stop_{i}"):
                stop_task(i)
                st.experimental_rerun()  # Rerun the script to reflect changes immediately

# Editable summary table
st.header("Summary")
if not st.session_state['tasks'].empty:
    edited_df = st.data_editor(st.session_state['tasks'], num_rows="dynamic", key="summary_editor")
    if edited_df is not None:
        st.session_state['tasks'] = edited_df
        save_tasks()

# Custom CSS for background color
st.markdown(
    """
    <style>
    .stApp {
        background-color: #c0c9d9;
    }
    </style>
    """,
    unsafe_allow_html=True
)
