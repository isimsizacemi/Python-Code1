import tkinter as tk
from tkinter import filedialog, messagebox, Listbox, Scrollbar


class FileComparisonView:
    """Tkinter arayüzünü yöneten View sınıfı."""

    def __init__(self, root, controller, root2):
        self.root = root
        self.root2 = root2
        self.controller = controller
        self.root.title("CSV Karşılaştırma Aracı")
        self.root.geometry("800x600")

        self.last_file_path = tk.StringVar()
        self.new_file_path = tk.StringVar()
        self.key_columns = tk.StringVar()
        self.svn_file_range = tk.StringVar()
        self.compare_file_path = tk.StringVar()

        # Son CSV dosyasını seçmek için bileşenler
        tk.Label(root, text="Last CSV File : ").pack(pady=5)
        self.entry_last_file = tk.Entry(root, textvariable=self.last_file_path, width=50, state=tk.NORMAL)
        self.entry_last_file.pack(pady=5)

        button_last_file = tk.Button(root, text="Gözat", command=self.controller.select_last_file)
        button_last_file.pack(pady=5)

        # Yeni CSV dosyasını seçmek için bileşenler
        tk.Label(root, text="New CSV File : ").pack(pady=5)
        self.entry_new_file = tk.Entry(root, textvariable=self.new_file_path, width=50, state=tk.NORMAL)
        self.entry_new_file.pack(pady=5)

        button_new_file = tk.Button(root, text="Gözat", command=self.controller.select_new_file)
        button_new_file.pack(pady=5)

        # Kullanıcıdan anahtar sütunları alma alanı
        tk.Label(root, text="Karşılaştırma için Anahtar Sütunları (virgülle ayırarak yazın):").pack(pady=5)
        self.entry_key_columns = tk.Entry(root, textvariable=self.key_columns, width=50, state=tk.NORMAL)
        self.entry_key_columns.pack(pady=5)

        # Dosyaları karşılaştırma butonu
        tk.Button(root, text="Karşılaştır", command=self.controller.compare_files).pack(pady=10)

        # Karşılaştırma sonuçlarını gösterecek Listbox ve Scrollbar
        self.logListBox = Listbox(root, width=100, height=10)
        self.logListBox.pack(pady=5)

        scrollbar = Scrollbar(root, command=self.logListBox.yview)
        scrollbar.pack(side="right", fill="y")
        self.logListBox.config(yscrollcommand=scrollbar.set)

        # SVN loglarını gösterecek Listbox ve Scrollbar
        tk.Label(self.root2, text="RANGE ENTER:").pack(pady=5)
        self.svn_entry = tk.Entry(self.root2, textvariable=self.svn_file_range, width=50, state=tk.NORMAL)
        self.svn_entry.pack(pady=5)

        self.fetch_logs_button = tk.Button(self.root2, text="SVN Logları Getir", command=self.controller.fetch_svn_logs)
        self.fetch_logs_button.pack(pady=10)

        self.logListBoxMenu = Listbox(self.root2, width=100, height=10)
        self.logListBoxMenu.pack(side="left", fill="y", pady=5)

        scrollbarMenu = Scrollbar(self.root2, command=self.logListBoxMenu.yview)
        scrollbarMenu.pack(side="right", fill="y")
        self.logListBoxMenu.config(yscrollcommand=scrollbarMenu.set)

        # Yeni CSV dosyasını seçmek için bileşenler
        tk.Label(root2, text="New CSV File : ").pack(pady=5)
        self.entry_compare_file = tk.Entry(root2, textvariable=self.compare_file_path, width=50, state=tk.NORMAL)
        self.entry_compare_file.pack(pady=5)

        button_compare_file = tk.Button(root2, text="Gözat", command=self.controller.select_compare_file)
        button_compare_file.pack(pady=5)

    def select_file(self):
        """Dosya seçme penceresini açar ve kullanıcıya dosya seçtirir."""
        return filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv"), ("All Files", "*.*")])

    def get_compare_file_path(self):
        return self.compare_file_path.get()

    def update_compare_file_path(self, path):
        """Seçilen dosya yolunu Entry widget'ına manuel olarak yazdırır."""
        print(f"Güncellenen Dosya Yolu (insert ile): {path}")  # Debug için ekledik
        self.compare_file_path.set(path)  # StringVar Güncellemesi
        self.entry_compare_file.delete(0, tk.END)  # Önce temizle
        self.entry_compare_file.insert(0, path)  # Sonra yeni yolu ekle

    def update_last_file_path(self, path):
        """Seçilen last.csv dosyasının yolunu günceller."""
        self.last_file_path.set(path)

    def update_new_file_path(self, path):
        """Seçilen new.csv dosyasının yolunu günceller."""
        self.new_file_path.set(path)

    def get_last_file_path(self):
        """Son sürüm CSV dosya yolunu döndürür."""
        return self.last_file_path.get()

    def get_new_file_path(self):
        """Yeni sürüm CSV dosya yolunu döndürür."""
        return self.new_file_path.get()

    def display_logs(self, logs):
        """Karşılaştırma sonuçlarını Listbox içinde gösterir."""
        self.logListBox.delete(0, tk.END)
        for log in logs:
            self.logListBox.insert(tk.END, f"{log['key']}: {log['message']}")

    def show_error(self, message):
        """Hata mesajı gösterir."""
        messagebox.showerror("Hata", message)

    def get_key_columns(self):
        """Kullanıcının girdiği anahtar sütunları döndürür."""
        return [col.strip() for col in self.key_columns.get().split(',') if col.strip()]

    def get_svn_file_range(self):
        """SVN giriş alanındaki değeri alır ve kontrol eder."""
        value = self.svn_file_range.get().strip()
        if not value:
            self.show_error("Lütfen SVN için bir aralık girin!")
            return None
        try:
            return int(value)  # Eğer sayıysa integer olarak döndür
        except ValueError:
            self.show_error("SVN Aralığı sadece sayısal bir değer olmalıdır!")
            return None

    def display_svn_files(self, logs):
        """SVN tarafından kaydedilen CSV dosyalarının isimlerini gösterir."""
        self.logListBoxMenu.delete(0, tk.END)
        if not logs:
            self.logListBoxMenu.insert(tk.END, "SVN logları bulunamadı.")
            return
        for file_name in logs:
            self.logListBoxMenu.insert(tk.END, file_name)
