import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import os
import shutil
import webbrowser
from threading import Thread

class BackupApp:
    def __init__(self, master):
        self.master = master
        master.title("BackupBliss - Herramienta de Backup Automático")
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.configure_styles()

        self.frame = ttk.Frame(master)
        self.frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(self.frame, text="Seleccione la carpeta SourceData para hacer backup:").pack()
        self.source_path_entry = ttk.Entry(self.frame, width=50)
        self.source_path_entry.pack(pady=5)
        ttk.Button(self.frame, text="SourceData", command=self.browse_source_folder).pack()

        ttk.Label(self.frame, text="Seleccione la carpeta DataBackup del backup:").pack()
        self.destination_path_entry = ttk.Entry(self.frame, width=50)
        self.destination_path_entry.pack(pady=5)
        ttk.Button(self.frame, text="DataBackup", command=self.browse_destination_folder).pack()

        self.progress = tk.DoubleVar()
        ttk.Label(self.frame, text="Progreso:").pack()
        self.progress_bar = ttk.Progressbar(self.frame, length=200, variable=self.progress, mode='determinate')
        self.progress_bar.pack(pady=10)

        ttk.Button(self.frame, text="Crear Copia de Seguridad", command=self.start_backup_thread).pack(pady=5)
        
        ttk.Button(self.frame, text="YouTube", command=self.open_youtube_and_thank).pack(side=tk.LEFT, padx=(0,10))
        ttk.Button(self.frame, text="Whatsapp", command=self.open_whatsapp_and_thank).pack(side=tk.LEFT)

        ttk.Button(self.frame, text="Donar con Nequi", command=lambda: self.show_donation_info('Nequi', '3174615279')).pack(side=tk.RIGHT, padx=(10,0))
        ttk.Button(self.frame, text="Donar con Daviplata", command=lambda: self.show_donation_info('DaviPlata', '3174615279')).pack(side=tk.RIGHT)
    
    def open_link(self, url):
       webbrowser.open(url)

    def open_youtube_and_thank(self):
        messagebox.showinfo("Gracias", "¡Gracias por visitar mi canal de YouTube!")
        self.open_link('https://www.youtube.com/channel/UCU0RNCbxnXCJ9SlrqUz-8eg')

    def open_whatsapp_and_thank(self):
        messagebox.showinfo("Contacto", "¡Gracias por ponerte en contacto a través de WhatsApp!")
        self.open_link('https://wa.me/+573173539733')

    def configure_styles(self):
        self.style.configure('TFrame', background='gray20')
        self.style.configure('TButton', background='gray30', foreground='white', font=('Helvetica', 10))
        self.style.configure('TLabel', background='gray20', foreground='white', font=('Helvetica', 10))
        self.style.configure('TEntry', foreground='gray60', font=('Helvetica', 10))
        self.style.configure('Horizontal.TProgressbar', background='light green')
        self.master.configure(bg='gray20')
        self.credit_label = tk.Label(self.master, text="@Kevin - JJ", bg="lightgrey", anchor='se')
        self.credit_label.pack(fill=tk.X, side=tk.BOTTOM, ipady=2)

    def browse_source_folder(self):
        folder_selected = filedialog.askdirectory()
        if folder_selected:
            self.source_path_entry.delete(0, tk.END)
            self.source_path_entry.insert(0, folder_selected)

    def browse_destination_folder(self):
        folder_selected = filedialog.askdirectory()
        if folder_selected:
            self.destination_path_entry.delete(0, tk.END)
            self.destination_path_entry.insert(0, folder_selected)

    def start_backup_thread(self):
        backup_thread = Thread(target=self.create_backup)
        backup_thread.start()

    def create_backup(self):
        source_folder = self.source_path_entry.get()
        destination_folder = self.destination_path_entry.get()
        if not os.path.exists(destination_folder):
            os.makedirs(destination_folder)
        files = os.listdir(source_folder)
        total_files = len(files)

        folders = {
            'PDF': ['.pdf'],
            'Word': ['.doc', '.docx'],
            'Excel': ['.xls', '.xlsx'],
            'Fotos': ['.jpg', '.jpeg', '.png', '.gif'],
            'Videos': ['.mp4', '.mov', '.avi']
        }

        for folder, extensions in folders.items():
            os.makedirs(os.path.join(destination_folder, folder), exist_ok=True)

        for index, file in enumerate(files):
            source_file = os.path.join(source_folder, file)
            file_ext = os.path.splitext(file)[1].lower()
            dest_folder = next((f for f, exts in folders.items() if file_ext in exts), "Otros")
            os.makedirs(os.path.join(destination_folder, dest_folder), exist_ok=True)
            destination_path = os.path.join(destination_folder, dest_folder, file)
            if os.path.isfile(source_file):
                shutil.copy2(source_file, destination_path)
            self.progress.set((index + 1) / total_files * 100)
            self.master.update_idletasks()

        messagebox.showinfo("Backup Completo", "La copia de seguridad se completó exitosamente.")

    def show_donation_info(self, platform, account_number):
        messagebox.showinfo("Donar", f"Plataforma: {platform}\nNúmero de cuenta: {account_number}\n¡Gracias por tu donación a Kevin - JJ! Tu apoyo es muy apreciado.")

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("600x400")
    root.resizable(False, False)
    app = BackupApp(root)
    root.mainloop()
