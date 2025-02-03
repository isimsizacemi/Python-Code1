import subprocess
import os
import re

repo_url = "https://svn.example.com/repo"  # SVN deponuzun URL'si
save_dir = "saved_files"  # Dosyaların kaydedileceği klasör

command = ["svn", "log", "-l", "10", "-v", repo_url]
process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
stdout, stderr = process.communicate()

if process.returncode != 0:
    print(stderr.decode())
    exit()

output = stdout.decode()
revisions = {}

for block in re.split(r"^-{40,}$", output):
    if block.strip():
        lines = block.strip().splitlines()
        revision = lines[0].split("|")[0].strip()
        revisions[revision] = []
        for line in lines:
            if line.startswith("M ") or line.startswith("A "):
                file_path = line.split(" ")[1].strip()
                revisions[revision].append(file_path)

for revision, files in revisions.items():
    for file_path in files:
        local_path = os.path.join(save_dir, revision, file_path)
        os.makedirs(os.path.dirname(local_path), exist_ok=True)
        svn_command = ["svn", "export", "-r", revision, repo_url + file_path, local_path]
        subprocess.run(svn_command)
