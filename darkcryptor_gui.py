# ================================
# DarkCryptor CLI Tool
# Version: 1.0
# Author: super66x
# GitHub: https://github.com/super66x
# Description: Command-line tool to encrypt, obfuscate, and optionally compile Python scripts to EXE.
# ================================

import customtkinter as ctk
from tkinter import filedialog
import os
import threading
from darkcryptor_core import process_encryption  # Core encryption logic

# Set theme and appearance
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

class DarkCryptorGUI(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Window configuration
        self.title("DarkCryptor # Version: 1.0 | Coder: super66x")
        self.geometry("720x560")

        # Header label
        self.header = ctk.CTkLabel(self, text="DarkCryptor", font=ctk.CTkFont(size=26, weight="bold"))
        self.header.pack(pady=15)

        # Dark mode toggle (Light/Dark/System)
        self.darkmode_var = ctk.StringVar(value=ctk.get_appearance_mode())
        self.darkmode_switch = ctk.CTkOptionMenu(
            self, values=["Light", "Dark", "System"],
            variable=self.darkmode_var,
            command=self.change_appearance_mode
        )
        self.darkmode_switch.pack(pady=(0, 10))

        # About button (shows about dialog)
        self.about_btn = ctk.CTkButton(self, text="❓", width=30, height=30, command=self.show_about)
        self.about_btn.pack(pady=(0, 10))

        # File selection frame
        self.file_frame = ctk.CTkFrame(self)
        self.file_frame.pack(fill="x", padx=15, pady=5)

        self.file_path_var = ctk.StringVar()
        self.file_entry = ctk.CTkEntry(self.file_frame, textvariable=self.file_path_var)
        self.file_entry.pack(side="left", fill="x", expand=True, padx=(10,5), pady=10)

        self.browse_btn = ctk.CTkButton(self.file_frame, text="Browse File", command=self.browse_file)
        self.browse_btn.pack(side="right", padx=(5,10), pady=10)

        # Template selection
        self.template_var = ctk.StringVar(value="none")
        self.template_frame = ctk.CTkFrame(self)
        self.template_frame.pack(fill="x", padx=15, pady=5)
        ctk.CTkLabel(self.template_frame, text="Template:").pack(side="left", padx=10)

        self.template_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "templates")
        templates_list = ["none"] + [os.path.splitext(f)[0] for f in os.listdir(self.template_dir) if f.endswith(".py")] if os.path.isdir(self.template_dir) else ["none"]

        self.template_dropdown = ctk.CTkOptionMenu(self.template_frame, values=templates_list, variable=self.template_var)
        self.template_dropdown.pack(side="left", padx=10)

        # Obfuscation level selection
        self.obf_var = ctk.StringVar(value="none")
        self.obf_frame = ctk.CTkFrame(self)
        self.obf_frame.pack(fill="x", padx=15, pady=5)
        ctk.CTkLabel(self.obf_frame, text="Obfuscation:").pack(side="left", padx=10)
        for level in ["none", "basic", "advanced"]:
            ctk.CTkRadioButton(self.obf_frame, text=level.capitalize(), variable=self.obf_var, value=level).pack(side="left", padx=5)

        # EXE conversion checkbox
        self.to_exe_var = ctk.BooleanVar(value=False)
        self.exe_check = ctk.CTkCheckBox(self, text="Convert to EXE", variable=self.to_exe_var, command=self.toggle_icon_select)
        self.exe_check.pack(anchor="w", padx=25, pady=5)

        # Icon selection (visible only when EXE option is selected)
        self.icon_path_var = ctk.StringVar()
        self.icon_frame = ctk.CTkFrame(self)
        self.icon_frame.pack(fill="x", padx=25, pady=5)
        self.icon_frame.pack_forget()  # Initially hidden

        ctk.CTkLabel(self.icon_frame, text="Icon (.ico):").pack(side="left", padx=5)
        self.icon_entry = ctk.CTkEntry(self.icon_frame, textvariable=self.icon_path_var)
        self.icon_entry.pack(side="left", fill="x", expand=True, padx=5)
        self.icon_browse_btn = ctk.CTkButton(self.icon_frame, text="Browse", command=self.browse_icon)
        self.icon_browse_btn.pack(side="left", padx=5)

        # Output directory selection
        self.output_dir_var = ctk.StringVar(value=os.path.join(os.getcwd(), "output"))
        os.makedirs(self.output_dir_var.get(), exist_ok=True)

        self.output_frame = ctk.CTkFrame(self)
        self.output_frame.pack(fill="x", padx=15, pady=5)
        ctk.CTkLabel(self.output_frame, text="Output Directory:").pack(side="left", padx=10)
        self.output_entry = ctk.CTkEntry(self.output_frame, textvariable=self.output_dir_var)
        self.output_entry.pack(side="left", fill="x", expand=True, padx=5)
        self.output_browse_btn = ctk.CTkButton(self.output_frame, text="Browse", command=self.browse_output_dir)
        self.output_browse_btn.pack(side="left", padx=5)

        # Log output box
        self.logbox = ctk.CTkTextbox(self, height=150, wrap="word")
        self.logbox.pack(fill="both", expand=True, padx=15, pady=10)

        # Start encryption button
        self.encrypt_btn = ctk.CTkButton(self, text="Encrypt", command=self.start_encrypt)
        self.encrypt_btn.pack(pady=15)

    # Change theme appearance
    def change_appearance_mode(self, choice):
        ctk.set_appearance_mode(choice)

    # File browser for Python scripts
    def browse_file(self):
        file = filedialog.askopenfilename(filetypes=[("Python Files", "*.py")])
        if file:
            self.file_path_var.set(file)

    # Icon file browser (.ico only)
    def browse_icon(self):
        ico = filedialog.askopenfilename(filetypes=[("Icon files", "*.ico")])
        if ico:
            self.icon_path_var.set(ico)

    # Output directory browser
    def browse_output_dir(self):
        folder = filedialog.askdirectory()
        if folder:
            self.output_dir_var.set(folder)

    # Toggle icon selection based on EXE checkbox
    def toggle_icon_select(self):
        if self.to_exe_var.get():
            self.icon_frame.pack(fill="x", padx=25, pady=5)
        else:
            self.icon_frame.pack_forget()
            self.icon_path_var.set("")

    # Append text to log output
    def log(self, text):
        self.logbox.insert("end", text + "\n")
        self.logbox.see("end")

    # Start encryption in a separate thread
    def start_encrypt(self):
        threading.Thread(target=self.encrypt, daemon=True).start()

    # Main encryption logic: validates inputs, calls process_encryption, logs results/errors
    def encrypt(self):
        source = self.file_path_var.get()
        if not source or not os.path.isfile(source):
            self.log("[!] Please select a valid Python file.")
            return
        try:
            result = process_encryption(
                source_file=source,
                output_dir=self.output_dir_var.get(),
                template_dir=self.template_dir,
                template=self.template_var.get(),
                obf_level=self.obf_var.get(),
                to_exe=self.to_exe_var.get(),
                icon_path=self.icon_path_var.get() if self.to_exe_var.get() else None
            )
            self.log(f"[+] Encryption successful! Output: {result}")
        except Exception as e:
            self.log(f"[!] Error: {e}")

    # About popup window
    def show_about(self):
        about_window = ctk.CTkToplevel(self)
        about_window.title("About")
        about_window.geometry("400x300")
        about_window.resizable(False, False)

        ctk.CTkLabel(about_window, text="DarkCryptor", font=ctk.CTkFont(size=24, weight="bold")).pack(pady=15)
        ctk.CTkLabel(about_window, text="Version: 1.0").pack(pady=5)
        ctk.CTkLabel(about_window, text="Coder: super66x").pack(pady=5)
        ctk.CTkLabel(about_window, text="Description:\nأpython encryption tool EXE", justify="center").pack(pady=15)
        ctk.CTkButton(about_window, text="إغلاق", command=about_window.destroy).pack(pady=20)

# Launch the GUI app
if __name__ == "__main__":
    app = DarkCryptorGUI()
    app.mainloop()
