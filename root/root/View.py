
import tkinter as tk
from tkinter import filedialog , messagebox 
from tkinter import Listbox , Scrollbar


class FileCompilerView:
        
    def __init__(self, root, controller , toplevel):
        self.root = root
        self.controller = controller
        self.root.title("TAI Compiler Module Two File Compiler")
        self.root.geometry("800x600")
        
        self.last_file_path = tk.StringVar(value= r"C:\Users\s22722\Desktop\New folder\last.csv")
        self.new_file_path = tk.StringVar(value= r"C:\Users\s22722\Desktop\New folder\new.csv")
        self.key_columns= tk.StringVar(value="Enum,Main")       
        self.log_version_range =  tk.StringVar(value="10")    
        self.compare_file_path = tk.StringVar(value=r"C:\Users\s22722\Desktop\New folder\last.csv")
        
        
        tk.Label(root , text="LAST CSV :").pack(pady=5)
        tk.Entry(root , textvariable=self.last_file_path).pack(pady=5)
        button_last_file = tk.Button(root,text = 'Browse', command = self.controller.select_last_file)
        button_last_file.pack(pady=5)
        
        tk.Label(root , text="NEW CSV :").pack(pady=5)
        tk.Entry(root , textvariable=self.new_file_path).pack(pady=5)
        button_new_file = tk.Button(root,text = 'Browse', command = self.controller.select_new_file)
        button_new_file.pack(pady=5)
        
        tk.Label(root , text="Enter Keys").pack(pady=5)
        tk.Entry(root , textvariable=self.key_columns).pack(pady=5)
        
        
        compared_button= tk.Button(root , text="Compiler" , command= self.controller.compare_file)
        compared_button.pack(pady=5)
        
        
        
        self.logListBox = Listbox(root, width=300 , height=50)
        self.logListBox.pack(pady=5)
        scrollBar = Scrollbar(root , command= self.logListBox.yview)
        scrollBar.pack(side="left" , fill="y")
        self.logListBox.config(yscrollcommand=scrollBar.set)

        
                ## HOME --------------------------------------------
        self.toplevel = toplevel ## Top level
        self.toplevel.title("TAI Compiler Module HOME")
        self.toplevel.geometry("800x600")
        
        tk.Label(toplevel , text="----Home Page----").pack(pady=5)
        self.logListBoxHome = Listbox(toplevel,width=80 , height=50)
        self.logListBoxHome.pack(pady=5,side="left" , fill="y")
    
        
        scrollBarHome = Scrollbar(toplevel , command= self.logListBoxHome.yview)
        scrollBarHome.pack(side="left" , fill="y")
        self.logListBoxHome.config(yscrollcommand=scrollBarHome.set)
        
        tk.Label(toplevel , text="Enter Keys").pack(pady=5)
        tk.Entry(toplevel , textvariable=self.key_columns).pack(pady=5)
        
        tk.Label(toplevel , text="Select to Compare Files").pack(pady=5)
        self.entry_compare_file = tk.Entry(toplevel , textvariable=self.compare_file_path  , state=tk.NORMAL ) 
        self.entry_compare_file.pack(pady=5)
        button_compare_file = tk.Button(toplevel ,text = 'Browse', command = self.controller.select_compare_file)
        button_compare_file.pack(pady=5)
        
        tk.Label(toplevel , text="Log Version Range :").pack(pady=5)
        self.log_entry = tk.Entry(toplevel )
        self.log_entry.pack(pady=5)
        tk.Button(toplevel , text="Loggeeeed" , command= self.controller.set_log_range).pack(pady=5)
        
        
        # ---------------------------
        
        #tk.Button(toplevel , text = "Open Selected CSV File ", command = self.controller.selected_sv_log)
        
        
    def get_log_version_range(self):
        return self.log_entry.get()
    
    def select_file(self):
        return filedialog.askopenfilename(title="Select a File", filetypes=[("Text files", "*.csv"), ("All files", "*.*")])
    
    def update_last_file_path(self, path):        
        self.last_file_path.set(path)
        
    def get_last_file_path(self):
        return self.last_file_path.get()
    
    def update_new_file_path(self,path):
        self.new_file_path.set(path)
        
    def get_compare_file_path(self):
        return self.compare_file_path.get()
        
    def update_compare_file_path(self,path):
          self.compare_file_path.set(path)
          self.entry_compare_file.delete(0 , tk.END)
          self.entry_compare_file.insert(0 , path)

    
    
    def get_new_file_path(self):
        return self.new_file_path.get()
    
    def error_show(self,message):
        messagebox.showerror("ERROR" , message)
        
    def get_key_columns(self):
        return [col.strip() for col in self.key_columns.get().split(',') if col.strip()]
    

    def display_logs(self,logs):
        self.logListBox.delete(0 , tk.END)
        
        for log in logs:            
            self.logListBox.insert(tk.END , f"{log}")
        
    def display_svn_logs(self,svn_log):
        self.logListBoxHome.delete(0 , tk.END)
        
        for log in svn_log:            
            self.logListBoxHome.insert(tk.END , f"{log}")
    
    
    
    
        
        
        
        
        
        