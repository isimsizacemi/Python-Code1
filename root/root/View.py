import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import Listbox, Scrollbar

class FileCompilerView:
    def __init__(self, root, controller, toplevel):
        self.root = root
        self.controller = controller
        self.root.title("File Compiler")
        self.root.geometry("800x600")

        self.last_file_path = tk.StringVar()
        self.new_file_path = tk.StringVar()
        self.key_columns = tk.StringVar()
        self.log_version_range = tk.StringVar()
        self.compare_file_path = tk.StringVar()

        tk.Label(root, text="Last CSV:").pack(pady=5)
        tk.Entry(root, textvariable=self.last_file_path).pack(pady=5)
        tk.Button(root, text="Browse", command=self.controller.select_last_file).pack(pady=5)

        tk.Label(root, text="New CSV:").pack(pady=5)
        tk.Entry(root, textvariable=self.new_file_path).pack(pady=5)
        tk.Button(root, text="Browse", command=self.controller.select_new_file).pack(pady=5)

        tk.Label(root, text="Enter Keys:").pack(pady=5)
        tk.Entry(root, textvariable=self.key_columns).pack(pady=5)

        tk.Button(root, text="Compare", command=self.controller.compare_file).pack(pady=5)

        self.logListBox = Listbox(root, width=100, height=20)
        self.logListBox.pack(pady=5)
        scrollBar = Scrollbar(root, command=self.logListBox.yview)
        scrollBar.pack(side="left", fill="y")
        self.logListBox.config(yscrollcommand=scrollBar.set)

    def select_file(self):
        return filedialog.askopenfilename(title="Select a File", filetypes=[("CSV files", "*.csv"), ("All files", "*.*")])

    def update_last_file_path(self, path):
        self.last_file_path.set(path)

    def update_new_file_path(self, path):
        self.new_file_path.set(path)

    def get_last_file_path(self):
        return self.last_file_path.get()

    def get_new_file_path(self):
        return self.new_file_path.get()

    def get_key_columns(self):
        return [col.strip() for col in self.key_columns.get().split(",") if col.strip()]

    def display_logs(self, logs):
        self.logListBox.delete(0, tk.END)
        for log in logs:
            self.logListBox.insert(tk.END, f"{log}")
