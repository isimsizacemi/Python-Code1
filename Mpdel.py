import csv
import json
import os
import subprocess


class FileComparisonModel:
    """Dosya karşılaştırma ve SVN log işlemlerini gerçekleştiren model sınıfı."""

    def __init__(self):
        self.last_file = None  # Karşılaştırılacak son CSV dosyası
        self.new_file = None  # Karşılaştırılacak yeni CSV dosyası
        self.key_columns = []  # Karşılaştırma için kullanılacak anahtar sütunlar

    def set_files(self, last_file, new_file):
        """Karşılaştırılacak dosyaları ayarlar."""
        self.last_file = last_file
        self.new_file = new_file

    def set_key_columns(self, key_columns):
        """Karşılaştırma için anahtar sütunları ayarlar."""
        self.key_columns = key_columns

    def read_csv(self, file_path):
        """CSV dosyasını okuyup bir liste halinde döndürür."""
        data = []
        try:
            with open(file_path, mode="r", encoding="utf-8") as file:
                reader = csv.reader(file)
                headers = next(reader)  # İlk satırı başlıklar olarak al
                for row in reader:
                    data.append(dict(zip(headers, row)))  # Başlıkları ve satır verilerini eşleştir
        except Exception as e:
            raise Exception(f"CSV dosyası okunurken hata oluştu: {e}")
        return data

    def create_key(self, row):
        """Belirtilen sütunları birleştirerek bir anahtar oluşturur."""
        return "_".join(row.get(col, "N/A") for col in self.key_columns)

    def compare_files(self):
        """İki CSV dosyasını karşılaştırarak değişiklikleri döndürür."""
        if not self.last_file or not self.new_file:
            raise Exception("Hem son hem de yeni dosya seçilmiş olmalıdır.")

        last_data = {self.create_key(row): row for row in self.read_csv(self.last_file)}
        new_data = {self.create_key(row): row for row in self.read_csv(self.new_file)}

        logs = []

        # Silinen veya değiştirilen satırlar
        for key, last_row in last_data.items():
            if key not in new_data:
                logs.append({"key": key, "message": f"DELETED: {last_row}"})
            elif last_row != new_data[key]:
                for col in last_row.keys():
                    if last_row[col] != new_data[key][col]:
                        logs.append({
                            "key": key,
                            "message": f"Changed Column: {col} | Last: {last_row[col]} -> New: {new_data[key][col]}"
                        })

        # Eklenen satırlar
        for key, new_row in new_data.items():
            if key not in last_data:
                logs.append({"key": key, "message": f"ADDED: {new_row}"})

        return logs

    def save_logs(self, logs, log_file="log.json"):
        """Karşılaştırma sonuçlarını JSON formatında kaydeder."""
        try:
            with open(log_file, "w", encoding="utf-8") as file:
                json.dump(logs, file, indent=4)
            return log_file
        except Exception as e:
            raise Exception(f"JSON log dosyası kaydedilirken hata oluştu: {e}")

    def save_as_txt(self, logs, output_file="changes.txt"):
        """Karşılaştırma sonuçlarını TXT formatında kaydeder."""
        try:
            with open(output_file, "w", encoding="utf-8") as file:
                for log in logs:
                    file.write(f"{log['key']}: {log['message']}\n")
            return output_file
        except Exception as e:
            raise Exception(f"TXT dosyası kaydedilirken hata oluştu: {e}")

    def fetch_svn_logs(self, username, password, svn_range, svn_path="."):
        """SVN loglarını almak için subprocess kullanır."""
        try:
            cmd = ["svn", "log", svn_path, "--username", username, "--password", password, "-l", str(svn_range), "--non-interactive"]
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            return result.stdout
        except subprocess.CalledProcessError as e:
            raise Exception(f"SVN logları alınırken hata oluştu: {e}")

    def parse_svn_logs(self, logs):
        """SVN loglarını işleyerek versiyon listesini döndürür."""
        versions = []
        for line in logs.splitlines():
            if line.startswith("r") and "|" in line:
                versions.append(line.split(" | ")[0])  # Versiyon numarasını al
        return versions

    def save_logs_to_csv(self, logs, output_file="svn_logs.csv"):
        """SVN loglarını CSV formatında kaydeder."""
        try:
            with open(output_file, "w", encoding="utf-8", newline="") as file:
                writer = csv.writer(file)
                writer.writerow(["Version"])  # Sütun başlıkları
                for log in logs:
                    writer.writerow([log])
            return output_file
        except Exception as e:
            raise Exception(f"CSV dosyası kaydedilirken hata oluştu: {e}")

    def download_file_by_version(self, username, password, file_path, version, output_dir="downloaded_files"):
        """SVN'den belirli bir versiyona ait dosyayı indirir."""
        try:
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)
            output_file = os.path.join(output_dir, f"{os.path.basename(file_path)}_r{version}")
            cmd = ["svn", "export", f"{file_path}@{version}", output_file, "--username", username, "--password", password, "--non-interactive"]
            subprocess.run(cmd, check=True)
            return output_file
        except Exception as e:
            raise Exception(f"Dosya indirilemedi: {e}")
