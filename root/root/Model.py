import csv
import json
import subprocess
import os

class FileCompilerModel:
    def __init__(self):
        self.key = None
        self.file_list = None

    @staticmethod
    def create_key(row, key_columns):
        return "_".join(row[col] for col in key_columns)

    @staticmethod
    def read_csv_as_dict(file_path, key_columns):
        data = {}

        with open(file_path, "r", newline='', encoding="utf-8") as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                key = FileCompilerModel.create_key(row, key_columns)
                data[key] = row

        return data

    @staticmethod
    def compare_file(new_file, last_file, key_columns, log_file):
        last_data = FileCompilerModel.read_csv_as_dict(last_file, key_columns)
        new_data = FileCompilerModel.read_csv_as_dict(new_file, key_columns)

        changes = []

        with open(log_file, "w") as log:
            for last_key, last_row in last_data.items():
                if last_key in new_data:
                    new_row = new_data[last_key]
                    for col in last_row.keys():
                        if str(last_row[col]) != str(new_row[col]):
                            changes.append({
                                "key": last_key,
                                "message": f"Modified --> {col}: {last_row[col]} changes to -> {new_row[col]}"
                            })
                else:
                    changes.append({
                        "key": last_key,
                        "message": f"Deleted: {last_row}"
                    })

            for new_key, new_row in new_data.items():
                if new_key not in last_data:
                    changes.append({
                        "key": new_key,
                        "message": f"Added: {new_row}"
                    })

            json.dump(changes, log, indent=4)

        return changes if changes else "No Changes Found"

    def save_logs(self, logs, log_file="log.txt"):
        if not logs:
            return {"status": "No Changes Detected"}

        try:
            with open(log_file, "w") as file:
                json.dump(logs, file, indent=4)
            return {"status": "Saved"}
        except Exception:
            return {"status": "Error Saving"}
