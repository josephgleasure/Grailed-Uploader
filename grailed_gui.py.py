import tkinter as tk
from tkinter import ttk
import json
import subprocess

class SimpleDropGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Grailed Uploader")
        self.create_drop_zones()
        self.start_btn = ttk.Button(root, text="Start Upload", command=self.start_upload)
        self.start_btn.grid(row=4, column=0, pady=10)
        self.start_btn.grid_remove()
        self.files = {}
        
    def create_drop_zones(self):
        labels = ["Config", "Listings", "Images", "Measurements"]
        self.zones = {}
        
        for i, label in enumerate(labels):
            zone = ttk.Label(
                self.root, 
                text=f"Drop {label} here",
                relief="solid",
                padding=30
            )
            zone.grid(row=i, column=0, pady=5, padx=20, sticky="ew")
            zone.drop_target_register(tk.DND_FILES)
            zone.dnd_bind('<<Drop>>', lambda e, l=label: self.on_drop(e, l))
            self.zones[label] = zone
            
    def on_drop(self, event, zone_label):
        path = event.data.replace('{', '').replace('}', '')
        self.files[zone_label] = path
        self.zones[zone_label].configure(text=f"{zone_label} added ✓")
        
        if len(self.files) == 4:
            self.start_btn.grid()
            
    def start_upload(self):
        try:
            subprocess.run(["python", "grailed_uploader.py"])
            tk.messagebox.showinfo("Success", "Upload complete")
        except Exception as e:
            tk.messagebox.showerror("Error", str(e))

if __name__ == "__main__":
    root = tk.Tk()
    app = SimpleDropGUI(root)
    root.mainloop()