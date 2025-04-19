import tkinter as tk
from tkinter import messagebox
import json
import os

TASKS_FILE = "tasks.json"

def load_tasks():
    if not os.path.exists(TASKS_FILE):
        return []
    with open(TASKS_FILE, "r") as f:
        return json.load(f)

def save_tasks(tasks):
    with open(TASKS_FILE, "w") as f:
        json.dump(tasks, f, indent=4)

class ToDoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("To-Do List")
        self.root.geometry("500x300")
        self.root.resizable(False, False)

        self.tasks = load_tasks()
        self.task_var = tk.StringVar()

        # == Ana Çerçeve ==
        self.main_frame = tk.Frame(root)
        self.main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # == Sol Panel: Görev Listesi ==
        self.left_frame = tk.Frame(self.main_frame)
        self.left_frame.pack(side="left", fill="both", expand=True)

        self.listbox = tk.Listbox(self.left_frame, width=30, height=15, selectmode=tk.SINGLE)
        self.listbox.pack(side="left", fill="both", expand=True)

        self.scrollbar = tk.Scrollbar(self.left_frame)
        self.scrollbar.pack(side="right", fill="y")
        self.listbox.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.listbox.yview)

        # == Sağ Panel: Giriş ve Butonlar ==
        self.right_frame = tk.Frame(self.main_frame, padx=10)
        self.right_frame.pack(side="right", fill="y")

        self.entry = tk.Entry(self.right_frame, textvariable=self.task_var, width=25)
        self.entry.pack(pady=(0, 10))

        self.add_button = tk.Button(self.right_frame, text="Add Task", width=20, command=self.add_task)
        self.add_button.pack(pady=5)

        self.done_button = tk.Button(self.right_frame, text="Mark as Done", width=20, command=self.mark_done)
        self.done_button.pack(pady=5)

        self.delete_button = tk.Button(self.right_frame, text="Delete Task", width=20, command=self.delete_task)
        self.delete_button.pack(pady=5)

        self.refresh_list()
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    def refresh_list(self):
        self.listbox.delete(0, tk.END)
        for task in self.tasks:
            status = "✔" if task['done'] else "✘"
            self.listbox.insert(tk.END, f"[{status}] {task['text']}")

    def add_task(self):
        text = self.task_var.get().strip()
        if text:
            self.tasks.append({"text": text, "done": False})
            self.task_var.set("")
            self.refresh_list()
        else:
            messagebox.showwarning("Input Error", "Task cannot be empty.")

    def mark_done(self):
        idx = self.listbox.curselection()
        if idx:
            self.tasks[idx[0]]['done'] = True
            self.refresh_list()
        else:
            messagebox.showwarning("Selection Error", "Select a task first.")

    def delete_task(self):
        idx = self.listbox.curselection()
        if idx:
            del self.tasks[idx[0]]
            self.refresh_list()
        else:
            messagebox.showwarning("Selection Error", "Select a task first.")

    def on_close(self):
        save_tasks(self.tasks)
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = ToDoApp(root)
    root.mainloop()
