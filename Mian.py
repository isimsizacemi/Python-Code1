import tkinter as tk
from controller import FileComparisonController


def main():
    """Uygulamayı başlatır."""
    # İki ayrı root pencere tanımlıyoruz
    root2 = tk.Tk()  # İlk açılacak pencere (SVN log ekranı)

    # Controller'ı başlat
    controller = FileComparisonController(root2)

    # Uygulamanın çalışmasını başlat
    root2.mainloop()


if __name__ == "__main__":
    main()
