# -*- coding: utf-8 -*-
"""
Created on Tue Feb  4 12:03:51 2025

@author: s22722
"""

    
    @staticmethod
    def export_revisions( revisions , path):
        export_file_path = r"C:\Users\s22722\Desktop\Compare\Compare"
        FILE_PATH = path
        
        log_output = subprocess.check_output(f"svn log -l {range_version} --verbose {FILE_PATH}", shell = True , text  = True)
        
        revision = []
        
        for line in log_output.split("\n"):
            if line.startswith("r") and line[1].isdigit():
                rev_num = line.split()[0][1:]
                revision.append(rev_num)
            
        
        for rev in revision : 
            file_name = os.path.basename(FILE_PATH)
            export_file_path = os.path.join(export_dir , f"{file_name}_rev{rev}")
            
            export_cmd = f"svn cat -r {rev} \"{FILE_PATH}\" > \"{export_file_path}\""
            subprocess.run(export_cmd , shell=True , check=True)
            
        print(f"Son {len(revision)} revizyon '{export_dir}' saved")
        
        
        
        def set_log_range(self):
            log_range = self.view.get_log_version_range()
          
            self.log_version_range = log_range
            
            if self.log_version_range:
             #  svn_log = self.model.get_svn_log(self.log_version_range, self.view.compare_file_path) #file_list , comapre file 
               
               # compiler ı ayağa kaldırıp ordan alınan bu listeyi 0 dan 10 a kadar sıra sıra loglıcam
               log_version = self.model.svn_log_revisions(self.log_version_range, self.view.compare_file_path) #file_list , compare file 
               
               self.model.export_revisions(log_version ,self.view.compare_file_path )
               
               self.view.display_svn_logs(log_version)
               
               for version , path in (len(log_version) -1) :
                   
                   new_version_path = svn_log[i]["file_path"]
                   last_version_path = svn_log[i+1]["file_path"]
                   log_file = f"{svn_log[i+1]["version"]} vs {svn_log[i]["version"]}_log.txt "
                   
                   self.svn_logs_compare(new, last, log_file)
                   
                   
        
        
        
        
    
    
    
    @staticmethod
    def saved_svn_log(revisions):
        SAVEPATH = r"C:\Users\s22722\Desktop\Compare\Compare\svnLogFiles"
        
        if not revisions:
            return
        
        os.mkdirs(SAVEPATH , exis_ok=True)
        
        for rev in revisions:
            output_path = os.path.join(SAVEPATH , f"version_{rev}.txt")
            
            subprocess.run(["svn", "export", "-r", rev , SVN_FILE_PATH , output_path])
