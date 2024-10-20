import tkinter as tk
from tkinter import messagebox, PhotoImage
import pickle
from PIL import Image, ImageTk
import itertools

# Initialize the main window
root = tk.Tk()
root.title("To-Do List App")
root.geometry("800x800")
root.config(bg="black")

# Global list to store tasks
tasks = []

# Save and Load functions for tasks
def save_tasks():
    with open("tasks.pkl", "wb") as file:
        pickle.dump(tasks, file)

def load_tasks():
    global tasks
    try:
        with open("tasks.pkl", "rb") as file:
            tasks = pickle.load(file)
            update_task_list()
    except FileNotFoundError:
        tasks = []

# Update the task list
def update_task_list():
    task_listbox.delete(0, tk.END)
    for task in tasks:
        task_listbox.insert(tk.END, task)
        if task.startswith("✔️"):
            task_listbox.itemconfig(tk.END, {'bg': '#1f5130', 'fg': 'white'})
        else:
            task_listbox.itemconfig(tk.END, {'bg': '#4A4A8A', 'fg': 'white'})

# Add a new task
def add_task():
    task = task_entry.get().strip()
    if task:
        tasks.append(task)
        update_task_list()
        task_entry.delete(0, tk.END)
        save_tasks()
    else:
        messagebox.showwarning("Warning", "Task cannot be empty!")

def remove_task():
    try:
        selected_index = task_listbox.curselection()[0]
        task_listbox.delete(selected_index)
        tasks.pop(selected_index)
        save_tasks()
    except IndexError:
        messagebox.showwarning("Warning", "Select a task to remove.")

def complete_task():
    try:
        selected_index = task_listbox.curselection()[0]
        tasks[selected_index] = f"✔️ {tasks[selected_index]}"
        update_task_list()
        save_tasks()
    except IndexError:
        messagebox.showwarning("Warning", "Select a task to mark as completed.")

def clear_all_tasks():
    if messagebox.askyesno("Clear All", "Are you sure you want to clear all tasks?"):
        tasks.clear()
        update_task_list()
        save_tasks()

# Load icons
add_icon = Image.open("adds.png").resize((32, 32), Image.LANCZOS)
add_icon = ImageTk.PhotoImage(add_icon)

remove_icon = Image.open("remove.png").resize((32, 32), Image.LANCZOS)
remove_icon = ImageTk.PhotoImage(remove_icon)

complete_icon = Image.open("done.png").resize((32, 32), Image.LANCZOS)
complete_icon = ImageTk.PhotoImage(complete_icon)

clear_icon = Image.open("clear.png").resize((32, 32), Image.LANCZOS)
clear_icon = ImageTk.PhotoImage(clear_icon)

# Create GUI components
# Title label and images
title_frame = tk.Frame(root, bg="black")
title_frame.place(relx=0.5, rely=0.1, anchor='center')  # Add space from the top

# Load and add Pikachu image
pikachu_image = Image.open("char.png").resize((120, 85), Image.LANCZOS)  # Adjust size accordingly
pikachu_image = ImageTk.PhotoImage(pikachu_image)
pikachu_label = tk.Label(title_frame, image=pikachu_image, bg="black")
pikachu_label.pack(side="left")

# Title label with DJ lights effect
title_label = tk.Label(title_frame, text="My To-Do List", font=("Arial", 36, "bold"), bg="black", fg="white")
title_label.pack(side="left", padx=10)

# Load and add To-Do image
todo_image = Image.open("todo.png").resize((120, 85), Image.LANCZOS)  # Adjust size accordingly
todo_image = ImageTk.PhotoImage(todo_image)
todo_label = tk.Label(title_frame, image=todo_image, bg="black")
todo_label.pack(side="right")

# DJ Lights effect for title
def dj_lights_effect():
    colors = ['#FF4500', '#FFD700', '#00BFFF', '#FF69B4', '#8A2BE2']
    color_cycle = itertools.cycle(colors)
    def change_color():
        title_label.config(fg=next(color_cycle))
        root.after(500, change_color)  # Change color every 500 ms
    change_color()

dj_lights_effect()  # Start DJ lights effect

# Create task entry and buttons
task_entry = tk.Entry(root, width=40, font=("Arial", 18), bg="#4A4A8A", fg="white")
task_entry.place(relx=0.1, rely=0.2, relwidth=0.8)

button_frame = tk.Frame(root, bg="black")
button_frame.place(relx=0.1, rely=0.3, relwidth=0.8)

# Create button frame and center it
button_frame = tk.Frame(root, bg="black")
button_frame.place(relx=0.5, rely=0.3, anchor='center', relwidth=0.8)

# Configure grid columns for equal weight
for i in range(4):  # Assuming you have 4 buttons
    button_frame.grid_columnconfigure(i, weight=1)

add_button = tk.Button(button_frame, image=add_icon, text=" Add Task", compound="left", command=add_task, 
                       bg="#4CAF50", fg="white", font=("Arial", 13, "bold"))
add_button.grid(row=0, column=0, padx=5, sticky='ew')

remove_button = tk.Button(button_frame, image=remove_icon, text=" Remove Task", compound="left", command=remove_task, 
                          bg="#f44336", fg="white", font=("Arial", 13, "bold"))
remove_button.grid(row=0, column=1, padx=5, sticky='ew')

complete_button = tk.Button(button_frame, image=complete_icon, text=" Mark Completed", compound="left", 
                            command=complete_task, bg="#2196F3", fg="white", font=("Arial", 13, "bold"))
complete_button.grid(row=0, column=2, padx=5, sticky='ew')

clear_button = tk.Button(button_frame, image=clear_icon, text=" Clear All", compound="left", command=clear_all_tasks, 
                         bg="#FF9800", fg="white", font=("Arial", 13, "bold"))
clear_button.grid(row=0, column=3, padx=5, sticky='ew')

# Create a frame for the task listbox with a white/silver border
task_frame = tk.Frame(root, bg="white")
task_frame.place(relx=0.1, rely=0.4, relwidth=0.8, relheight=0.5)

task_listbox = tk.Listbox(task_frame, font=("Arial", 16), selectmode=tk.SINGLE, bg="black", fg="white")
task_listbox.pack(expand=True, fill='both', padx=5, pady=5)  # Padding inside the box

# Load tasks on startup
load_tasks()

# Start the GUI event loop
root.mainloop()
