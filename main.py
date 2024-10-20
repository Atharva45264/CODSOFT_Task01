import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import pickle
import itertools

# Initialize window
root = tk.Tk()
root.title("To-Do List")
root.geometry("800x800")
root.config(bg="black")

tasks = []

def save():
    with open("tasks.pkl", "wb") as f:
        pickle.dump(tasks, f)

def load():
    global tasks
    try:
        with open("tasks.pkl", "rb") as f:
            tasks = pickle.load(f)
        refresh()
    except FileNotFoundError:
        tasks = []

def refresh():
    task_box.delete(0, tk.END)
    for t in tasks:
        task_box.insert(tk.END, t)
        color = '#1f5130' if t.startswith("✔️") else '#4A4A8A'
        task_box.itemconfig(tk.END, {'bg': color, 'fg': 'white'})

# Added the warning windows
def add():
    task = entry.get().strip()
    if task:
        tasks.append(task)
        refresh()
        entry.delete(0, tk.END)
        save()
    else:
        messagebox.showwarning("Warning", "Task cannot be empty!")

def remove():
    try:
        idx = task_box.curselection()[0]
        task_box.delete(idx)
        tasks.pop(idx)
        save()
    except IndexError:
        messagebox.showwarning("Warning", "Select a task to remove.")

def complete():
    try:
        idx = task_box.curselection()[0]
        tasks[idx] = f"✔️ {tasks[idx]}"
        refresh()
        save()
    except IndexError:
        messagebox.showwarning("Warning", "Select a task to complete.")

def clear():
    if messagebox.askyesno("Clear All", "Are you sure you want to clear all tasks?"):
        tasks.clear()
        refresh()
        save()

def animate_title():
    colors = ['#FF4500', '#FFD700', '#00BFFF', '#FF69B4', '#8A2BE2']
    cycle = itertools.cycle(colors)

    def change():
        title_lbl.config(fg=next(cycle))
        root.after(500, change)

    change()

# Loaded icons and resized them
def load_icon(path):
    img = Image.open(path).resize((32, 32), Image.LANCZOS)
    return ImageTk.PhotoImage(img)

add_img = load_icon("adds.png")
remove_img = load_icon("remove.png")
done_img = load_icon("done.png")
clear_img = load_icon("clear.png")

# Added header with image and title
header = tk.Frame(root, bg="black")
header.place(relx=0.5, rely=0.1, anchor='center')

char_img = Image.open("char.png").resize((120, 85), Image.LANCZOS)
char_icon = ImageTk.PhotoImage(char_img)
char_lbl = tk.Label(header, image=char_icon, bg="black")
char_lbl.pack(side="left")

title_lbl = tk.Label(header, text="My To-Do List", font=("Arial", 36, "bold"), bg="black", fg="white")
title_lbl.pack(side="left", padx=10)

todo_img = Image.open("todo.png").resize((120, 85), Image.LANCZOS)
todo_icon = ImageTk.PhotoImage(todo_img)
todo_lbl = tk.Label(header, image=todo_icon, bg="black")
todo_lbl.pack(side="right")

animate_title()

entry = tk.Entry(root, width=40, font=("Arial", 18), bg="#4A4A8A", fg="white")
entry.place(relx=0.1, rely=0.2, relwidth=0.8)

btn_frame = tk.Frame(root, bg="black")
btn_frame.place(relx=0.5, rely=0.3, anchor='center', relwidth=0.8)

for i in range(4):
    btn_frame.grid_columnconfigure(i, weight=1)

tk.Button(btn_frame, image=add_img, text=" Add", compound="left", command=add, 
          bg="#4CAF50", fg="white", font=("Arial", 13, "bold")).grid(row=0, column=0, padx=5, sticky='ew')

tk.Button(btn_frame, image=remove_img, text=" Remove", compound="left", command=remove, 
          bg="#f44336", fg="white", font=("Arial", 13, "bold")).grid(row=0, column=1, padx=5, sticky='ew')

tk.Button(btn_frame, image=done_img, text=" Complete", compound="left", command=complete, 
          bg="#2196F3", fg="white", font=("Arial", 13, "bold")).grid(row=0, column=2, padx=5, sticky='ew')

tk.Button(btn_frame, image=clear_img, text=" Clear All", compound="left", command=clear, 
          bg="#FF9800", fg="white", font=("Arial", 13, "bold")).grid(row=0, column=3, padx=5, sticky='ew')

task_frame = tk.Frame(root, bg="white")
task_frame.place(relx=0.1, rely=0.4, relwidth=0.8, relheight=0.5)

task_box = tk.Listbox(task_frame, font=("Arial", 16), selectmode=tk.SINGLE, bg="black", fg="white")
task_box.pack(expand=True, fill='both', padx=5, pady=5)

load()

root.mainloop()

