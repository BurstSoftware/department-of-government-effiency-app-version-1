import streamlit as st
import pandas as pd
from datetime import datetime
import json

class EfficiencyTracker:
    def __init__(self):
        # Initialize session state for tasks if not exists
        if 'tasks' not in st.session_state:
            st.session_state.tasks = []

    def _save_tasks(self):
        """Save tasks to file or browser storage equivalent"""
        try:
            with open('tasks.json', 'w') as f:
                json.dump(st.session_state.tasks, f)
        except Exception as e:
            st.error(f"Error saving tasks: {e}")

    def _load_tasks(self):
        """Load tasks from file or browser storage equivalent"""
        try:
            with open('tasks.json', 'r') as f:
                st.session_state.tasks = json.load(f)
        except FileNotFoundError:
            st.session_state.tasks = []
        except Exception as e:
            st.error(f"Error loading tasks: {e}")

    def add_task(self, task_text):
        """Add a new task to the list"""
        if task_text.strip():
            new_task = {
                'id': datetime.now().timestamp(),
                'text': task_text,
                'completed': False,
                'created_at': datetime.now().isoformat()
            }
            st.session_state.tasks.append(new_task)
            self._save_tasks()

    def delete_task(self, task_id):
        """Delete a task by its ID"""
        st.session_state.tasks = [
            task for task in st.session_state.tasks 
            if task['id'] != task_id
        ]
        self._save_tasks()

    def toggle_task_completion(self, task_id):
        """Toggle task completion status"""
        for task in st.session_state.tasks:
            if task['id'] == task_id:
                task['completed'] = not task['completed']
        self._save_tasks()

    def edit_task(self, task_id, new_text):
        """Edit an existing task"""
        for task in st.session_state.tasks:
            if task['id'] == task_id:
                task['text'] = new_text
        self._save_tasks()

    def get_efficiency_metrics(self):
        """Calculate efficiency metrics"""
        total_tasks = len(st.session_state.tasks)
        completed_tasks = sum(1 for task in st.session_state.tasks if task['completed'])
        
        completion_rate = (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0
        
        return {
            'total_tasks': total_tasks,
            'completed_tasks': completed_tasks,
            'completion_rate': round(completion_rate, 2)
        }

def main():
    st.set_page_config(
        page_title="Efficiency Tracker",
        page_icon="📊",
        layout="centered"
    )

    # Initialize tracker
    tracker = EfficiencyTracker()

    # Title
    st.title("📊 Efficiency Tracker")

    # Efficiency Metrics
    metrics = tracker.get_efficiency_metrics()
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(label="Total Tasks", value=metrics['total_tasks'])
    
    with col2:
        st.metric(label="Completed", value=metrics['completed_tasks'])
    
    with col3:
        st.metric(label="Completion Rate", value=f"{metrics['completion_rate']}%")

    # Task Input
    with st.form(key='task_form'):
        task_input = st.text_input("Enter a new task")
        submit_button = st.form_submit_button(label='Add Task')
        
        if submit_button and task_input:
            tracker.add_task(task_input)
            st.experimental_rerun()

    # Task List
    st.subheader("Your Tasks")
    
    if st.session_state.tasks:
        for task in st.session_state.tasks:
            col1, col2, col3 = st.columns([0.1, 0.7, 0.2])
            
            with col1:
                # Checkbox for task completion
                completed = st.checkbox(
                    label='', 
                    value=task['completed'], 
                    key=f"task_{task['id']}_complete"
                )
                if completed != task['completed']:
                    tracker.toggle_task_completion(task['id'])
            
            with col2:
                # Task text (strikethrough if completed)
                task_text = st.text_input(
                    label='Task', 
                    value=task['text'], 
                    key=f"task_{task['id']}_text",
                    disabled=task['completed']
                )
                
                # Check if task text was edited
                if task_text != task['text'] and not task['completed']:
                    tracker.edit_task(task['id'], task_text)
            
            with col3:
                # Delete button
                if st.button('Delete', key=f"task_{task['id']}_delete"):
                    tracker.delete_task(task['id'])
                    st.experimental_rerun()

    else:
        st.info("No tasks yet. Add a task to get started!")

if __name__ == "__main__":
    main()

# Optional: requirements.txt content
"""
streamlit==1.29.0
"""
