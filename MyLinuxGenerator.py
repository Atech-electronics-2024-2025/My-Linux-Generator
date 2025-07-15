import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json
import os
import subprocess
import threading
import time
from PIL import Image

class LinuxGarageApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("My Linux Generator")
        self.geometry("900x700")

        self.config_dir = "app_config"
        if not os.path.isdir(self.config_dir):
         if os.path.exists(self.config_dir):
            os.remove(self.config_dir)  # It was a file; remove it
            os.makedirs(self.config_dir)

        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill='both', expand=True)

        self._init_tabs()

    def _init_tabs(self):
        self._init_theme_tab()
        self._init_build_tab()

    def _init_theme_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text='Appearance & Layout')

        self.gtk_theme = tk.StringVar()
        self.icon_theme = tk.StringVar()
        self.layout_style = tk.StringVar()
        self.wallpaper_path = tk.StringVar()

       

        ttk.Button(tab, text="Select Wallpaper", command=self.choose_wallpaper).pack(pady=10)
        self.wallpaper_label = ttk.Label(tab, text="No file selected")
        self.wallpaper_label.pack()

        ttk.Button(tab, text="Save Appearance Settings", command=self.save_theme).pack(pady=10)
        ttk.Label(tab, text="Set Start Menu Icon (applicationsmenu.png):").pack()
        ttk.Button(tab, text="Select Icon", command=self.set_icon_standard).pack(pady=5)

        ttk.Label(tab, text="Set Start Menu Icon (applicationsmenu-hi.png):").pack()
        ttk.Button(tab, text="Select Hi-Res Icon", command=self.set_icon_hi).pack(pady=5)

        ttk.Label(tab, text="Set Boot Splash (bootlogo.png):").pack()
        ttk.Button(tab, text="Select Splash Image", command=self.set_splash_screen).pack(pady=5)
        ttk.Label(tab, text="Set Startup Sound (startup.wav):").pack()
        ttk.Button(tab, text="Select Startup Sound", command=self.set_startup_sound).pack(pady=5)

        ttk.Label(tab, text="Set Shutdown Sound (shutdown.wav):").pack()
        ttk.Button(tab, text="Select Shutdown Sound", command=self.set_shutdown_sound).pack(pady=5)


    def set_startup_sound(self):
      path = filedialog.askopenfilename(filetypes=[("WAV files", "*.wav")])
      if path:
        dest = os.path.join("Slax", "slackware15", "modules", "03-desktop", "rootcopy", "usr", "share", "sounds", "startup.wav")
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        try:
            with open(path, "rb") as src, open(dest, "wb") as dst:
                dst.write(src.read())
            messagebox.showinfo("Startup Sound Set", "startup.wav set successfully.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to set startup sound:\n{e}")

    def set_shutdown_sound(self):
     path = filedialog.askopenfilename(filetypes=[("WAV files", "*.wav")])
     if path:
        dest = os.path.join("Slax", "slackware15", "modules", "03-desktop", "rootcopy", "usr", "share", "sounds", "shutdown.wav")
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        try:
            with open(path, "rb") as src, open(dest, "wb") as dst:
                dst.write(src.read())
            messagebox.showinfo("Shutdown Sound Set", "shutdown.wav set successfully.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to set shutdown sound:\n{e}")


    def _init_build_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text='Build')

        ttk.Label(tab, text="Click below to start building your custom ISO:").pack(pady=10)
        ttk.Button(tab, text="Build ISO", command=self.start_build_thread).pack(pady=10)

        self.progress = ttk.Progressbar(tab, mode='determinate', maximum=100)
        self.progress.pack(fill='x', padx=20, pady=10)

        self.log_output = tk.Text(tab, height=15)
        self.log_output.pack(fill='both', expand=True, padx=10, pady=10)
    
        def set_icon_standard(self):
         path = filedialog.askopenfilename(filetypes=[("PNG Images", "*.png *.PNG")])
         if path:
            dest = os.path.join("Slax", "slackware15", "modules", "03-desktop", "rootcopy", "usr", "share", "icons", "hicolor", "48x48", "apps", "org.xfce.panel.applicationsmenu.png")
            os.makedirs(os.path.dirname(dest), exist_ok=True)
            try:
                Image.open(path).save(dest, "PNG")
                messagebox.showinfo("Icon Set", "Standard start menu icon set successfully.")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to set standard icon:\n{e}")

        def set_icon_hi(self):
          path = filedialog.askopenfilename(filetypes=[("PNG Images", "*.png *.PNG")])
          if path:
            dest = os.path.join("Slax", "slackware15", "modules", "03-desktop", "rootcopy", "usr", "share", "icons", "hicolor", "48x48", "apps", "org.xfce.panel.applicationsmenu-hi.png")
            os.makedirs(os.path.dirname(dest), exist_ok=True)
            try:
                Image.open(path).save(dest, "PNG")
                messagebox.showinfo("Icon Set", "Hi-res start menu icon set successfully.")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to set hi-res icon:\n{e}")

    def set_splash_screen(self):
        path = filedialog.askopenfilename(filetypes=[("PNG Images", "*.png *.PNG")])
        if path:
            for folder in ["bootfiles", os.path.join("Slax", "slackware15", "bootfiles")]:
                dest = os.path.join(folder, "bootlogo.png")
                os.makedirs(folder, exist_ok=True)
                try:
                    Image.open(path).save(dest, "PNG")
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to copy to {folder}:\n{e}")
            messagebox.showinfo("Splash Screen Set", "bootlogo.png copied to both bootfiles folders.")

    def set_icon_standard(self):
         path = filedialog.askopenfilename(filetypes=[("PNG Images", "*.png *.PNG")])
         if path:
            dest = os.path.join("Slax", "slackware15", "modules", "03-desktop", "rootcopy", "usr", "share", "icons", "hicolor", "48x48", "apps", "org.xfce.panel.applicationsmenu.png")
            os.makedirs(os.path.dirname(dest), exist_ok=True)
            try:
                Image.open(path).save(dest, "PNG")
                messagebox.showinfo("Icon Set", "Standard start menu icon set successfully.")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to set standard icon:\n{e}")

    def set_icon_hi(self):
         path = filedialog.askopenfilename(filetypes=[("PNG Images", "*.png *.PNG")])
         if path:
            dest = os.path.join("Slax", "slackware15", "modules", "03-desktop", "rootcopy", "usr", "share", "icons", "hicolor", "48x48", "apps", "org.xfce.panel.applicationsmenu-hi.png")
            os.makedirs(os.path.dirname(dest), exist_ok=True)
            try:
                Image.open(path).save(dest, "PNG")
                messagebox.showinfo("Icon Set", "Hi-res start menu icon set successfully.")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to set hi-res icon:\n{e}")

    def set_splash_screen(self):
         path = filedialog.askopenfilename(filetypes=[("PNG Images", "*.png *.PNG")])
         if path:
            for folder in ["bootfiles", os.path.join("Slax", "slackware15", "bootfiles")]:
                dest = os.path.join(folder, "bootlogo.png")
                os.makedirs(folder, exist_ok=True)
                try:
                    Image.open(path).save(dest, "PNG")
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to copy to {folder}:\n{e}")
            messagebox.showinfo("Splash Screen Set", "bootlogo.png copied to both bootfiles folders.")

    def choose_wallpaper(self):
     path = filedialog.askopenfilename(
      filetypes=[("All image files", "*.png *.jpg *.jpeg *.PNG *.JPG *.JPEG"), ("All files", "*.*")]
     )
     if path:
        # Destination path
        dest_path = os.path.join("Slax", "slackware15", "modules", "03-desktop", "rootcopy", "usr", "share", "wallpapers", "slax_wallpaper.jpg")

        # Make sure destination directory exists
        os.makedirs(os.path.dirname(dest_path), exist_ok=True)

        # Convert and save as JPEG
        try:
            img = Image.open(path).convert("RGB")  # Convert to RGB to ensure JPEG compatibility
            img.save(dest_path, "JPEG")
            self.wallpaper_path.set(dest_path)
            self.wallpaper_label.config(text=dest_path)
            messagebox.showinfo("Wallpaper Set", f"Wallpaper saved to:\n{dest_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to convert/save image:\n{e}")

    def save_packages(self):
        selected = [pkg for pkg, var in self.pkg_vars.items() if var.get()]
        with open(os.path.join(self.config_dir, 'selected_packages.txt'), 'w') as f:
            f.write('\n'.join(selected))
        messagebox.showinfo("Saved", "Package list saved.")

    def save_de(self):
        selected = [de for de, var in self.de_vars.items() if var.get()]
        with open(os.path.join(self.config_dir, 'selected_de.txt'), 'w') as f:
            f.write('\n'.join(selected))
        messagebox.showinfo("Saved", "Desktop environment selection saved.")

    def save_theme(self):
        config = {
            "gtk_theme": self.gtk_theme.get(),
            "icon_theme": self.icon_theme.get(),
            "layout_style": self.layout_style.get(),
            "wallpaper": self.wallpaper_path.get()
        }
        with open(os.path.join(self.config_dir, 'theme.json'), 'w') as f:
            json.dump(config, f, indent=2)
        messagebox.showinfo("Saved", "Appearance settings saved.")

    def start_build_thread(self):
         threading.Thread(target=self.build_iso, daemon=True).start()

    def build_iso(self):
        self.progress['value'] = 0
        self.log_output.insert(tk.END, "Building...\n")

        try:
            steps = [
                ("Setting permissions in root directory...", "sudo chmod 777 *"),
                ("Setting permissions in initramfs...", "cd initramfs && sudo chmod 777 *"),
                ("Starting...", "cd .."),
                ("Running build script...", "sudo chmod +x ./build && sudo ./build")
            ]

            for i, (msg, cmd) in enumerate(steps):
                self.log_output.insert(tk.END, msg + "\n")
                self.progress['value'] = int((i + 1) / len(steps) * 100)
                self.update_idletasks()
                subprocess.run(cmd, shell=True, check=True)
                time.sleep(0.5)  # Simulate delay

            self.log_output.insert(tk.END, "Build completed successfully.\n")
            self.progress['value'] = 100

        except subprocess.CalledProcessError as e:
            self.log_output.insert(tk.END, f"Build failed: {e}\n")
            self.progress['value'] = 0





if __name__ == "__main__":
    app = LinuxGarageApp()
    app.mainloop()
