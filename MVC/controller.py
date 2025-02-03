from model import FileComparisonModel
from view import FileComparisonView

import subprocess

class FileComparisonController:
    """Kullanıcı arayüzü ve model arasındaki bağlantıyı sağlayan denetleyici sınıf."""

    def __init__(self, root , root2):
        self.model = FileComparisonModel()  # Eksik parantez düzeltildi
        self.view = FileComparisonView(root, self, root2)
        self.key_columns = []

    def fetch_svn_logs(self):
        """SVN loglarını Model'den alır ve View'e gönderir."""
        svn_range = self.view.get_svn_file_range()  # View'den SVN log sayısını al
        logs = self.model.get_svn_logs( svn_range)  # Model'den SVN loglarını çek
        print(svn_range)
        self.view.display_svn_files(logs)  # View'de göster


    def get_svn_log_range(self):
        self.svn_file_range = self.view.get_svn_file_range()

    def select_last_file(self):
        """Kullanıcının last.csv dosyasını seçmesini sağlar."""
        file_path = self.view.select_file()
        if file_path:
            self.view.update_last_file_path(file_path)

    def select_new_file(self):
        """Kullanıcının new.csv dosyasını seçmesini sağlar."""
        file_path = self.view.select_file()
        if file_path:
            self.view.update_new_file_path(file_path)

    def set_columns(self):
        """Kullanıcıdan anahtar sütunları alır."""
        key_columns = self.view.get_key_columns()
        if key_columns:  # file_path değil key_columns kontrol edilmeli
            self.key_columns = key_columns

    def select_compare_file(self):
        """Kullanıcının compare CSV dosyasını seçmesini sağlar."""
        file_path = self.view.select_file()
        if file_path:
            print(f"Seçilen Compare Dosyası: {file_path}")  # Debug için ekledik
            self.view.update_compare_file_path(file_path)

    def compare_files(self):
        """İki dosya arasındaki farkları karşılaştırır ve sonucu arayüze iletir."""
        last_file = self.view.get_last_file_path()  # Gereksiz parametre kaldırıldı
        new_file = self.view.get_new_file_path()

        if not last_file or not new_file:
            self.view.show_error("Lütfen karşılaştırılacak dosyaları seçin!")
            return

        # Kullanıcının girdiği anahtar sütunları al
        self.set_columns()

        if not self.key_columns:
            self.view.show_error("Lütfen karşılaştırma için en az bir anahtar sütun girin!")
            return

        logs = self.model.compare_files(last_file, new_file, self.key_columns)
        self.model.save_logs(logs, "log.txt")
        self.view.display_logs(logs)
