import csv
from tkinter import *
import tkinter as tk
from tkinter import filedialog
from Model import FileCompilerModel
from View import FileCompilerView



class FileCompilerController:
    def __init__(self,root,toplevel):
        self.model = FileCompilerModel()
        self.view  = FileCompilerView(root,self,toplevel)
        self.key_columns = []
        self.log_version_range = None
        self.svn_log_path= None
        
    
    def select_last_file(self):
        
        file_path = self.view.select_file()
        if file_path:
            self.view.update_last_file_path(file_path)
            
    def select_compare_file(self):
       
        file_path = self.view.select_file()
        
        print(file_path)
        if file_path :
            self.view.update_compare_file_path(file_path)
    
    def select_new_file(self):
        file_path = self.view.select_file()
        if file_path:
            self.view.update_new_file_path(file_path)
    
    def set_log_range(self):
        log_range = self.view.get_log_version_range()
      
        self.log_version_range = log_range
        
        if self.log_version_range:
           
            self.svn_log_path=self.view.get_compare_file_path()
           
            log_versions = self.model.svn_log_revisions(self.log_version_range, self.svn_log_path) #file_list , compare file 
            print("log",log_versions)
            file_list = self.model.export_revisions(log_versions ,self.svn_log_path)
            
            self.view.display_svn_logs(file_list["file_name"])
            
            for version  in (len(log_version) -1) :
                
                new_version_path = svn_log[i]["file_path"]
                last_version_path = svn_log[i+1]["file_path"]
                log_file = f"{svn_log[i+1]['version']} vs {svn_log[i]['version']}_log.txt "
                
                self.svn_logs_compare(new, last, log_file)
                print("success")
             
                
    def set_key_columns(self):
        
        keys = self.view.get_key_columns()
  
        if keys : 
            self.key_columns = keys
            print("key columns: ",self.key_columns)
    
    
    
    
    def compare_file(self):
        last_file = self.view.get_last_file_path() 
        new_file = self.view.get_new_file_path()
        compare_file = self.view.get_compare_file_path()
        print(compare_file)
        
        if not last_file or not new_file:
            self.view.error_show("File Not found ")
            
        self.set_key_columns()
        
        if not self.set_key_columns:
            self.view.error_show("No Key Columns")
            
            
        logs = self.model.compare_file(new_file , last_file , self.key_columns,log_file=r"C:/Users/s22722/Desktop/New folder/version-log/log.txt")
        self.model.save_logs(logs)
        self.view.display_logs(logs)
        
        
        
        
    def svn_logs_compare(self,new,last,log_file):
        last_file = last 
        new_file = new
        log_file = log_file
        
        
        if not last_file or not new_file:
            self.view.error_show("File Not found ")
            
        self.set_key_columns()
        
        if not self.set_key_columns:
            self.view.error_show("No Key Columns")
            
            
        logs = self.model.compare_file(new_file , last_file , self.key_columns,log_file)
        self.model.save_logs(logs)
        self.view.display_logs(logs)
        
        
   
    
   
    
         
    def selected_sv_log(self, event):
        selected = self.view.logListBoxHome.curselection()
        
        log_selected = self.view.logListBoxHome.get(selected)
        
        data = self.model.read_csv_as_dict(log_selected)
        self.view.display_selected_log(data)
        