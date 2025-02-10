import tkinter as tk
from tkinter import filedialog, messagebox, Listbox, Scrollbar


class FileComparisonView:
    """Tkinter tabanlı View sınıfı."""

    def __init__(self, root2, controller):
        self.root2 = root2
        self.controller = controller

        self.root1 = None  # CSV Karşılaştırma ekranı (root1) henüz oluşturulmadı

        # SVN ekranı için gerekli değişkenler
        self.svn_file_range = tk.StringVar()
        self.svn_username = tk.StringVar()
        self.svn_password = tk.StringVar()

        # SVN logları için UI oluşturma
        self.setup_svn_logs_ui()

    def setup_svn_logs_ui(self):
        """SVN logları için arayüz bileşenlerini oluşturur."""
        self.root2.title("SVN Log Görüntüleyici")
        self.root2.geometry("800x600")

        # Başlık
        tk.Label(self.root2, text="SVN Logları", font=("Arial", 16, "bold")).pack(pady=10)

        # Kullanıcı Adı
        tk.Label(self.root2, text="Kullanıcı Adı:").pack(pady=5)
        self.svn_username_entry = tk.Entry(self.root2, textvariable=self.svn_username, width=50)
        self.svn_username_entry.pack(pady=5)

        # Şifre
        tk.Label(self.root2, text="Şifre:").pack(pady=5)
        self.svn_password_entry = tk.Entry(self.root2, textvariable=self.svn_password, width=50, show="*")
        self.svn_password_entry.pack(pady=5)

        # SVN Aralığı
        tk.Label(self.root2, text="SVN Aralığı Girin (Örn: 5):").pack(pady=5)
        self.svn_entry = tk.Entry(self.root2, textvariable=self.svn_file_range, width=50)
        self.svn_entry.pack(pady=5)

        # SVN loglarını getir butonu
        tk.Button(self.root2, text="SVN Logları Getir", command=self.controller.fetch_svn_logs, bg="lightblue").pack(pady=10)

        # CSV Karşılaştırma ekranını aç butonu
        tk.Button(self.root2, text="CSV Karşılaştırma Ekranını Aç", command=self.open_root1, bg="lightgreen").pack(pady=10)

    def open_root1(self):
        """CSV karşılaştırma ekranını açar."""
        if not self.root1:
            self.root1 = tk.Toplevel(self.root2)
            self.root1.title("CSV Karşılaştırma Aracı")
            self.root1.geometry("900x700")

            # Başlık
            tk.Label(self.root1, text="CSV Karşılaştırma Aracı", font=("Arial", 16, "bold")).pack(pady=10)

            # Last File seçimi
            tk.Label(self.root1, text="Son CSV Dosyası:").pack(pady=5)
            self.last_file_path = tk.StringVar()
            self.last_file_entry = tk.Entry(self.root1, textvariable=self.last_file_path, width=70)
            self.last_file_entry.pack(pady=5)
            tk.Button(self.root1, text="Gözat", command=self.controller.select_last_file).pack(pady=5)

            # New File seçimi
            tk.Label(self.root1, text="Yeni CSV Dosyası:").pack(pady=5)
            self.new_file_path = tk.StringVar()
            self.new_file_entry = tk.Entry(self.root1, textvariable=self.new_file_path, width=70)
            self.new_file_entry.pack(pady=5)
            tk.Button(self.root1, text="Gözat", command=self.controller.select_new_file).pack(pady=5)

            # Key columns seçimi
            tk.Label(self.root1, text="Anahtar Sütunları Girin (virgülle ayırarak):").pack(pady=5)
            self.key_columns = tk.StringVar()
            self.key_columns_entry = tk.Entry(self.root1, textvariable=self.key_columns, width=70)
            self.key_columns_entry.pack(pady=5)

            # Karşılaştır butonu
            tk.Button(self.root1, text="Dosyaları Karşılaştır", command=self.controller.compare_files, bg="lightblue").pack(pady=10)

            # Sonuçları görüntülemek için Listbox
            tk.Label(self.root1, text="Karşılaştırma Sonuçları:").pack(pady=5)
            self.log_listbox = Listbox(self.root1, width=100, height=15)
            self.log_listbox.pack(pady=5)
            scrollbar = Scrollbar(self.root1, command=self.log_listbox.yview)
            scrollbar.pack(side="right", fill="y")
            self.log_listbox.config(yscrollcommand=scrollbar.set)

            # Kapat butonu
            tk.Button(self.root1, text="Kapat", command=self.close_root1, bg="red").pack(pady=10)

    def close_root1(self):
        """CSV Karşılaştırma ekranını kapatır."""
        if self.root1:
            self.root1.destroy()
            self.root1 = None

    def select_file(self):
        """Dosya seçme penceresini açar."""
        return filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv"), ("All Files", "*.*")])

    def update_last_file_path(self, path):
        """Son CSV dosyasının yolunu günceller."""
        self.last_file_path.set(path)

    def update_new_file_path(self, path):
        """Yeni CSV dosyasının yolunu günceller."""
        self.new_file_path.set(path)

    def get_key_columns(self):
        """Kullanıcının girdiği anahtar sütunları döndürür."""
        return [col.strip() for col in self.key_columns.get().split(',') if col.strip()]

    def get_svn_file_range(self):
        """SVN log aralığını döndürür."""
        try:
            return int(self.svn_file_range.get().strip())
        except ValueError:
            self.show_error("Lütfen geçerli bir SVN aralığı girin!")
            return None

    def get_svn_credentials(self):
        """SVN kullanıcı adı ve şifresini döndürür."""
        username = self.svn_username.get().strip()
        password = self.svn_password.get().strip()
        if not username or not password:
            self.show_error("Lütfen kullanıcı adı ve şifreyi doldurun!")
            return None, None
        return username, password

    def display_logs(self, logs):
        """Karşılaştırma sonuçlarını listede gösterir."""
        self.log_listbox.delete(0, tk.END)
        for log in logs:
            self.log_listbox.insert(tk.END, log)

    def show_error(self, message):
        """Hata mesajını gösterir."""
        messagebox.showerror("Hata", message)

    def show_info(self, message):
        """Bilgi mesajını gösterir."""
        messagebox.showinfo("Bilgi", message)
