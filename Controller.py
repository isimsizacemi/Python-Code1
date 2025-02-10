from model import FileComparisonModel
from view import FileComparisonView
import tkinter as tk


class FileComparisonController:
    """Controller sınıfı. Kullanıcı etkileşimlerini işler ve modeli yönetir."""

    def __init__(self, root2):
        self.model = FileComparisonModel()  # Model örneği
        self.view = FileComparisonView(root2, self)  # View örneği
        self.root1 = None  # CSV Karşılaştırma ekranı (root1) için tanımlama

    def select_last_file(self):
        """Son CSV dosyasını seç."""
        file_path = self.view.select_file()
        if file_path:
            self.model.last_file = file_path
            self.view.update_last_file_path(file_path)

    def select_new_file(self):
        """Yeni CSV dosyasını seç."""
        file_path = self.view.select_file()
        if file_path:
            self.model.new_file = file_path
            self.view.update_new_file_path(file_path)

    def compare_files(self):
        """İki dosyayı karşılaştır ve sonuçları görüntüle."""
        try:
            if not self.model.last_file or not self.model.new_file:
                self.view.show_error("Lütfen karşılaştırılacak dosyaları seçin!")
                return

            self.model.key_columns = self.view.get_key_columns()
            if not self.model.key_columns:
                self.view.show_error("Lütfen anahtar sütunları belirtin!")
                return

            logs = self.model.compare_files()
            self.model.save_logs(logs, "log.txt")
            self.model.save_as_txt(logs, "changes.txt")

            self.view.display_logs(logs)
            self.view.show_info("Dosyalar başarıyla karşılaştırıldı ve sonuçlar kaydedildi.")
        except Exception as e:
            self.view.show_error(f"Hata oluştu: {str(e)}")

    def fetch_svn_logs(self):
        """SVN loglarını getir ve sonuçları görüntüle."""
        try:
            username, password = self.view.get_svn_credentials()
            if not username or not password:
                return

            svn_range = self.view.get_svn_file_range()
            if not svn_range:
                return

            logs = self.model.fetch_svn_logs(username, password, svn_range)
            version_list = self.model.parse_svn_logs(logs)

            self.view.display_svn_files("\n".join(version_list))
            self.model.save_logs_to_csv(version_list, "svn_logs.csv")
            self.view.show_info("SVN logları başarıyla kaydedildi ve görüntülendi.")
        except Exception as e:
            self.view.show_error(f"SVN logları alınırken hata oluştu: {str(e)}")

    def download_file_by_version(self):
        """Belirli bir versiyona ait dosyayı indir."""
        try:
            username, password = self.view.get_svn_credentials()
            if not username or not password:
                return

            file_path = self.view.get_new_file_path()
            version = self.view.get_svn_file_range()  # Versiyon numarasını SVN loglarından alabilirsiniz
            if not file_path or not version:
                self.view.show_error("Lütfen dosya yolunu ve versiyonu belirtin!")
                return

            output_dir = "./downloaded_files"
            downloaded_file = self.model.download_file_by_version(username, password, file_path, version, output_dir)
            self.view.show_info(f"Dosya başarıyla indirildi: {downloaded_file}")
        except Exception as e:
            self.view.show_error(f"Dosya indirilirken hata oluştu: {str(e)}")

    def export_txt_logs(self):
        """Karşılaştırma sonuçlarını TXT olarak dışa aktar."""
        logs = self.view.log_listbox.get(0, tk.END)
        if logs:
            try:
                self.model.save_as_txt(logs, "exported_changes.txt")
                self.view.show_info("TXT dosyası başarıyla kaydedildi.")
            except Exception as e:
                self.view.show_error(f"TXT dosyası kaydedilirken hata oluştu: {str(e)}")

    def export_svn_logs(self):
        """SVN loglarını CSV olarak dışa aktar."""
        logs = self.view.logListBoxMenu.get(0, tk.END)
        if logs:
            try:
                self.model.save_logs_to_csv("\n".join(logs), "exported_svn_logs.csv")
                self.view.show_info("SVN logları CSV olarak başarıyla kaydedildi.")
            except Exception as e:
                self.view.show_error(f"SVN logları kaydedilirken hata oluştu: {str(e)}")

    def open_csv_comparison_screen(self):
        """CSV karşılaştırma ekranını açar."""
        if not self.root1:  # Eğer root1 zaten açıksa tekrar açılmasın
            self.root1 = tk.Toplevel()
            self.root1.title("CSV Karşılaştırma Ekranı")
            self.root1.geometry("900x700")
            self.view.setup_csv_comparison_ui(self.root1)
        else:
            self.root1.deiconify()  # root1 minimizeliyse geri getir

    def close_csv_comparison_screen(self):
        """CSV karşılaştırma ekranını kapatır."""
        if self.root1:
            self.root1.destroy()
            self.root1 = None
