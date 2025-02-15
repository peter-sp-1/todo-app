import tkinter as tk
from tkinter import messagebox
import sqlite3
from datetime import datetime

#Database setup
def init_db():
    conn = sqlite3.connect("tasks.db") #connecting to the db
    c = conn.cursor() #allow interaction with the db(CRUD)
    c.execute('''CREATE TABLE IF NOT EXISTS tasks
               (id INTEGER PRIMARY KEY, tasks TEXT, description TEXT, due_date TEXT, completed INTEGER)''')
    conn.commit() #saves new tasks to the database
    conn.close() #close the connection to the db

#Adding tasks to the db
def add_to_db(tasks, description, due_date):
    conn = sqlite3.connect("tasks.db")
    c = conn.cursor()
    c.execute("INSERT INTO tasks (tasks, description, due_date, completed) VALUES (?, ?, ?, ?)", (tasks, description, due_date, 0))
    conn.commit()
    conn.close()

#Listing tasks from the db
def get_tasks():
    conn = sqlite3.connect("tasks.db")
    c = conn.cursor()
    c.execute("SELECT * FROM tasks") #select all columns of all rows from the tasks table
    tasks = c.fetchall() # fetch all rows from the database
    conn.close() 
    return tasks #return the list of tasks

#Deleting tasks in the db
def delete_from_db(task_id):
    conn = sqlite3.connect("tasks.db")
    c = conn.cursor()
    c.execute("DELETE FROM tasks WHERE id=?", (task_id,))
    conn.commit()
    conn.close()

#Marking completed task in the db
def mark_task_completed(task_id):
    conn = sqlite3.connect("tasks.db")
    c = conn.cursor()
    c.execute("UPDATE tasks SET completed = 1 WHERE id=?", (task_id,)) 
    conn.commit()
    conn.close()


#GUI setup
class ToDoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("To-Do List App") #allows methods in the app to access the window.

        #Task Entry
        self.task_label = tk.Label(root, text="Task:")
        self.task_label.grid(row=0, column=0, padx=10, pady=5) 
        self.task_entry = tk.Entry(root, width=50)
        self.task_entry.grid(row=0, column=1, padx=10, pady=5)

        #Description
        self.desc_label = tk.Label(root, text="Description:")
        self.desc_label.grid(row=1, column=0, padx=10, pady=5) 
        self.desc_entry = tk.Entry(root, width=50)
        self.desc_entry.grid(row=1, column=1, padx=10, pady=5)

        #Due Date entry
        self.due_label = tk.Label(root, text="Due Date (YY-MM-DD):")
        self.due_label.grid(row=2, column=0, padx=10, pady=5) 
        self.due_entry = tk.Entry(root, width=50)
        self.due_entry.grid(row=2, column=1, padx=10, pady=5)

        #Buttons
        self.add_button = tk.Button(root, text="Add Task", command=self.add_task)
        self.add_button.grid(row=3, column=1, padx=10, pady=5, sticky="e")

        self.delete_button = tk.Button(root, text="Delete Task", command=self.delete_task)
        self.delete_button.grid(row=4, column=0, padx=10, pady=5)

        self.complete_button = tk.Button(root, text="Mark as Completed", command=self.mark_completed)
        self.complete_button.grid(row=4, column=1, padx=10, pady=5, sticky="e")

        #Listbox for tasks
        self.task_listbox = tk.Listbox(root, height=10, width=80)
        self.task_listbox.grid(row=5, column=0, columnspan=2, padx=10, pady=10)

         #Load tasks from database
        self.load_tasks()

    def add_task(self):
        task = self.task_entry.get()
        description = self.desc_entry.get()
        due_date = self.due_entry.get()

        if not task or not due_date:
            messagebox.showwarning("Input Error", "Task and Due Date are required")
            return
        
        try:
             #Validate Due Date format
             datetime.strptime(due_date, "%Y-%m-%d")
             add_to_db(task, description, due_date)
             self.load_tasks()
             self.task_entry.delete(0, tk.END)
             self.desc_entry.delete(0, tk.END)
             self.due_entry.delete(0, tk.END)

        except ValueError:
            messagebox.showerror("Invalid date", "Please enter the date in YYYY-MM-DD format")
        
    def load_tasks(self):
        self.task_listbox.delete(0, tk.END)
        tasks = get_tasks()
        for task in tasks:
            task_info = f"{task[1]} - {task[2]} (Due: {task[3]}) {'[Completed]' if task[4] else ''}"
            self.task_listbox.insert(tk.END, task_info)

    def delete_task(self):
        selected_task_index = self.task_listbox.curselection()
        
        if selected_task_index:  # If a task is selected
            task_id = get_tasks()[selected_task_index[0]][0]  # Get the task ID
            delete_from_db(task_id)  # Delete the task from the database
            self.load_tasks()  # Reload tasks to update the listbox
        else:  # If no task is selected
            messagebox.showwarning("Selection Error", "Please select a task")



    def mark_completed(self):
        selected_task_index = self.task_listbox.curselection()
        if selected_task_index:
            task_id = get_tasks()[selected_task_index[0]][0]  
            mark_task_completed(task_id) 
            self.load_tasks()  


if __name__ == "__main__":
    init_db()
    root = tk.Tk()  # Initialize the main Tkinter window
    app = ToDoApp(root)  # Pass the Tkinter window to the app class
    root.mainloop()