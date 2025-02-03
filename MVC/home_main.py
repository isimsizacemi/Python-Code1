import tkinter as tk
from controller import FileComparisonController

if __name__ == "__main__":
    root = tk.Tk()
    root2 = tk.Tk()
    app = FileComparisonController(root,root2)
    root2.mainloop()