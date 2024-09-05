✅ Work Tracker - V2.42
Work Tracker is a task management application built with Streamlit and Pandas, allowing users to create, track, and manage tasks efficiently. This app supports task creation, editing, tracking the start and end times, and archiving completed tasks.

Features
Add New Tasks: Input a task name, description, category, and priority.
Start/Stop Tasks: Start tracking the time for a task or mark it as completed.
Restart Task: Restart a completed task to continue working on it.
Archive Task: Archive completed tasks by moving them to a separate archive file.
Editable Summary Table: View and edit tasks dynamically from a summary table.
Data Persistence: Saves and loads tasks from CSV files, allowing you to pick up where you left off.
Installation
Clone the repository:

bash
Copy code
git clone https://github.com/your-username/worktracking.git
cd work-tracker
Set up a virtual environment:

bash
Copy code
python3 -m venv venv
source venv/bin/activate  # For Windows: venv\Scripts\activate
Install the dependencies:

bash
Copy code
pip install -r requirements.txt
Run the app:

bash
Copy code
streamlit run work_tracker.py
How to Use
Add a New Task
Enter the Task Name, Task Description, select the Category and Priority from the dropdown menus.
Click Add Task to save the task.
Manage Tasks
Each task is displayed as a card. You can:
Start Task: Click the button to start tracking time for a task.
Stop Task: Click the button to mark the task as completed and capture the end time.
Restart Task: For tasks that are completed, this button restarts the task.
Archive Task: This button will archive a completed task, moving it to an archive.csv file and removing it from the current task list.
Edit Tasks in the Summary Table
At the bottom of the app, you will see a Summary Table where you can:
Edit task details (such as description, category, priority, etc.) directly within the table.
Save any changes, which will automatically update the tasks.csv file.
Task Status Workflow
Not Started: The task has been added but not yet started.
Active: The task is currently in progress and being tracked.
Completed: The task has been completed and time tracking has stopped.
Archived: The task has been archived and moved to archive.csv.
Files
tasks.csv: Stores the current tasks.
archive.csv: Stores archived tasks.
Customization
Modify Task Categories
You can modify the available task categories by updating the list in the code:

python
Copy code
category = st.sidebar.selectbox("Category", ["Administration", "Project", "Support-App", "Support-Other", "Development", "Meetings", "Research", "Other"], key="category")
Add More Features
Notifications: You can implement notifications when tasks are due or past deadlines.
Enhanced Reporting: Generate reports on time spent on different categories.
Requirements
Python 3.7+
Streamlit
Pandas
To install the required dependencies, use:

bash
Copy code
pip install -r requirements.txt
License
This project is licensed under the MIT License - see the LICENSE file for details.