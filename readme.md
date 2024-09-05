# Work Tracker - V2.43

## Overview

**Work Tracker - V2.43** is a Streamlit-based web application designed to help you track your daily tasks efficiently. The app allows you to create, start, stop, and archive tasks, all in a user-friendly interface. You can also track your task history by archiving completed tasks and accessing them later.

## Features

- **Add New Task**: Easily add new tasks with descriptions, categories, and priorities.
- **Task Status**: Tasks can be started, stopped, or archived once completed.
- **Editable Summary**: View and edit tasks in a table format.
- **Task Cards**: Tasks are presented in individual cards for easy readability.
- **Archiving**: Completed tasks can be archived and stored in a separate CSV file.
- **Download Archive**: Archived tasks can be downloaded in CSV format.

## How to Use

### 1. Adding a Task
- Enter a task name, description, category, and priority on the sidebar.
- Click on the **Add Task** button at the bottom of the sidebar to add the task.

### 2. Starting a Task
- Each task can be started by clicking the **Start Task** button. This will timestamp the start time.

### 3. Stopping a Task
- Once a task is in progress, click **Stop Task** to end the task. This will record the end time and total time spent.

### 4. Archiving Completed Tasks
- Once a task is marked as completed, an **Archive Task** button appears.
- Clicking the **Archive Task** button will move the task to the archive and remove it from the active task list.

### 5. Viewing Archived Tasks
- Scroll down to the **Archived Tasks** section to view the list of archived tasks.
- You can download the archived tasks in CSV format using the **Download Archive CSV** button.

### 6. Editing Tasks
- In the **Summary** section, you can edit task details directly in the table.
- Any changes made will be saved automatically.

## Categories

The following categories are available for tasks:
- **Administration**
- **Project**
- **Support-App**
- **Support-Other**
- **Development**
- **Meetings**
- **Research**
- **Other**

## Priority Levels

You can assign one of the following priority levels to each task:
- **Low**
- **Medium**
- **High**

## Files

- `tasks.csv`: Stores the active tasks with all details.
- `archive.csv`: Stores the archived tasks that have been completed and removed from the active list.

## Installation

To set up the application locally:

1. Clone the repository:
   ```bash
   git clone https://github.com/thungong/worktracking.git

2. Navigate to the project directory:
cd worktracking

3. Install the required Python packages:
pip install -r requirements.txt

4. Run the Streamlit application:
streamlit run work_tracker.py

## Requirements
Python 3.7+
Streamlit: pip install streamlit
Pandas: pip install pandas
For detailed requirements, refer to the requirements.txt file.

## License
This project is licensed under the MIT License.