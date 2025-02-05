import csv
import json
from tkinter import *
import subprocess



class FileCompilerModel:
    
    def __init__(self):
        self.key = None
        self.file_list = None
        
        
    @staticmethod
    def create_key(row, key_columns):
      """Belirtilen sütunları birleştirerek bir anahtar oluşturur."""
      print(row)
      print("sds",key_columns)
      return "_".join(row[col] for col in key_columns)  # Eksik sütunlar için varsayılan değer "N/A"

            
    @staticmethod
    def read_csv_as_dict(file_path,key_columns):
    
        data={}
        
        with open(file_path, "r") as csv_file:
            reader = csv.reader(csv_file)
            next(reader)
            for row in reader:  
                key = FileCompilerModel.create_key(row, key_columns)
            
                data[key] = row
                
                
                
            reader = csv.DictReader(csv_file)
            
            for row in reader:  
                key = FileCompilerModel.create_key(row, key_columns)
                
                data[key] = row
        print(data)
        return data
    
    
    
    
    @staticmethod
    def compare_file(new_file,last_file,key_columns,log_file):
        last_data = {FileCompilerModel.create_key(row, key_columns): row for row in FileCompilerModel.read_csv_as_dict(last_file,key_columns)}
        new_data = {FileCompilerModel.create_key(row, key_columns): row for row in FileCompilerModel.read_csv_as_dict(new_file,key_columns)}

        #new_row_keys  = FileCompilerModel.read_csv_as_dict(new, key_columns) 
        #last_row_keys = FileCompilerModel.read_csv_as_dict(last, key_columns)  
        
        changes = []
       
        
        with open(log_file,"w") as log:
            
            for last_key , last_row in last_row_keys.items():
                    
                if last_key in new_row_keys:
                   
                    new_row = new_row_keys[last_key]
                    
                    for col in last_row.keys():
                
                        if str(last_row[col]) != str(new_row[col]):
                            
                            print(f"Modi  {col}: {last_row[col]} changes to -> {new_row[col]}")
                            changes.append({
                                "key"     : f"{last_key}",
                                "message" : f" Modified --> {col}: {last_row[col]} changes to -> {new_row[col]}" })                        
                else : 
                     
                     print(f"deleted : {last_row}")
                     changes.append({
                         "key"     : f"{last_key}",
                         "message" : f"  deleted  : {new_row}  "})
                    
            for new_key , new_row in new_row_keys.items():
        
               
                if new_key not in last_row_keys:
                  
                    print(f"added : {new_row}")
                    changes.append({
                            "key"     : f" {new_key}  ",
                            "message" : f"  added  : {new_row}  "})
            
            print(changes)
            if changes : 
                for values in changes:     
                    log.write(" ".join(["{}: {}".format(value_key, digit) for value_key, digit in values.items()]) + '\n')
                    
                    
                    return changes
                for values in changes:     
                    log.write(" ".join(["{}: {}".format(value_key, digit) for value_key, digit in values.items()]) + '\n')
            else : 
                    return "Cahanges File Not Found"

            
              #----------------------- bu kısım deneme kodları 

     
    
    @staticmethod    
    def svn_log_revisions( range_version , path):
        
        cmd = ["svn" ,"log" , "-l" ,str( range_version) , "--quiet" , path ]
        result = subprocess.run(cmd , stdout= subprocess.PIPE , stderr= subprocess.PIPE, text = True)
        
        if result.returncode != 10:
            print(result.stderr)
            return []
        
        
        logs = result.stdout.split("\n")
        revisions = [line.split()[0] [1:] for line in logs if line.startswith("r")]
        print(revisions)
        return revisions[:range_version]
    
    
    
    @staticmethod
    def export_revisions( revisions , path):
        export_file_path = r"C:\Users\s22722\Desktop\Compare\Compare"
        FILE_PATH = path
        
        os.mkdirs(export_file_path , exists_ok=True)
        
        file_list = []
                
        for rev in revisions : 
            file_name_rev = os.path.basename(FILE_PATH)
            export_file_path = os.path.join(export_file_path , f"{file_name_rev}_rev{rev}")
            
            file_list.append({
                    "file_name": f"{file_name_rev}",
                    "file_path": f"{export_file_path}"} )
            
            export_cmd = f"svn cat -r {rev} \"{FILE_PATH}\" > \"{export_file_path}\""
            subprocess.run(export_cmd ,stdout= subprocess.PIPE , stderr= subprocess.PIPE, text = True )
            
            
        print(f"Son {len(revisions)} revizyon '{export_file_path}' saved")
        
        return file_list
        
        

        
    @staticmethod
    def get_svn_log(log_version_range,file_path):  ## olmasada olur 
        file_list = []
        diff_files = []
        
        log = subprocess.run(
            ["svn" , "log" , file_path , "--non-interactive",  "--limit" ,str(log_version_range) ],
            stdout= subprocess.PIPE , stderr= subprocess.PIPE, text = True , Check=True
            )
                         # 3.6 and lsat version capture_output=True , text=True
        log_output = log.stdout
        
        file_list = log_output.split("\n")
        os.makedirs("svn_data", exis_ok = True)
        for line in logs :
            parts = line.stript().split()
            
            if len(parts) > 0 and parts[0].startswith("r") and parts[0][1:].isdigit():
                version_number = parts[0]
                file_path = f"svn_data/{version_number}.csv"
                if not os.path.exists(file_path):
                    os.makedirs(file_path)
                file_list.append(
                    {"version" : version_number,
                     "file_path" :  file_path
                     })
        
        return file_list
    
   
    
    def save_logs(logs,log_file="log.txt"):

        if not logs:
            return {"status" : "No Changes Detected, log file not creared"}
        
        
        try:
            with open(log_file , "w"  ) as file :
                json.dump(logs, file , indent=4)
            return {"status" : "Saved"}
         
        except Exception as e : 
                return {"status" : "Error Saving"}
       
       

         
         
     
     
     
     
     