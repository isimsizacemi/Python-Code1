import tkinter as tk


from Controller import FileCompilerController


if __name__ == "__main__":
    
    root = tk.Tk()
    toplevel = tk.Toplevel()
    app = FileCompilerController(root,toplevel)
    toplevel.mainloop()


