import csv
import json

class FileComparisonModel:
    """Dosya karşılaştırma işlemlerini yöneten model sınıfı."""

    @staticmethod
    def read_csv(file_path):
        """CSV dosyasını okuyup bir liste halinde döndürür."""
        data = []
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                reader = csv.DictReader(file)
                for i, row in enumerate(reader, start=1):  # Satır numarası ekliyoruz
                    row["line_number"] = i  # Satır numarasını kaydediyoruz
                    data.append(row)
        except Exception as e:
            return str(e)
        return data

    @staticmethod
    def create_key(row, key_columns):
        """Belirtilen sütunları birleştirerek bir anahtar oluşturur."""
        return "_".join(row.get(col, "N/A") for col in key_columns)  # Eksik sütunlar için varsayılan değer "N/A"

    @staticmethod
    def compare_files(last_file, new_file, key_columns):
        """İki CSV dosyasını karşılaştırarak değişiklikleri döndürür."""
        last_data = {FileComparisonModel.create_key(row, key_columns): row for row in FileComparisonModel.read_csv(last_file)}
        new_data = {FileComparisonModel.create_key(row, key_columns): row for row in FileComparisonModel.read_csv(new_file)}

        logs_dict = []

        if not last_data or not new_data:
            return [{"key": "ERROR", "message": "Dosya boş veya okunamıyor"}]  # Boş dosya kontrolü

        # Silinen ve değişen verileri kontrol et
        for key, last_row in last_data.items():
            if key not in new_data:
                logs_dict.append({"key": key, "line": last_row["line_number"], "message": f"DELETED: {last_row}"})
            elif last_row != new_data[key]:
                for col in last_row.keys():
                    if last_row[col] != new_data[key][col]:
                        logs_dict.append({
                            "key": key,
                            "line": last_row["line_number"],
                            "message": f"Changed Column: {col} | Last: {last_row[col]} -> New: {new_data[key][col]}"
                        })

        # Eklenen verileri kontrol et
        for key, new_row in new_data.items():
            if key not in last_data:
                logs_dict.append({"key": key, "line": new_row["line_number"], "message": f"ADDED: {new_row}"})

        return logs_dict

    @staticmethod
    def save_logs(logs, log_file="log.txt"):
        """Karşılaştırma sonuçlarını log dosyasına kaydeder."""
        if not logs:
            return {"status": "No changes detected, log file not created."}

        try:
            with open(log_file, "w", encoding="utf-8") as file:
                json.dump(logs, file, indent=4)
            return {"status": "Log file saved successfully.", "file": log_file}
        except Exception as e:
            return {"status": "Error saving log file.", "error": str(e)}


    @staticmethod
    def get_svn_logs(num_logs , svn_file_path="#" ):
        try:
            cmd= ["svn" , "log" , svn_file_path , "-l" , int(num_logs) ]
            print(cmd)
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            return result.stdout

        except :
            return f"Svn Log FAILED ! "