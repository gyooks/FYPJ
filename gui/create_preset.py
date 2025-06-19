import customtkinter as ctk
import os
import csv
import tkinter.messagebox as messagebox

class CreatePreset(ctk.CtkFrame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.label = ctk.CTkLabel(self, text="Create Preset")
        self.label.grid(row=0, column=0, padx=10, pady=10)

        self.entry = ctk.CTkEntry(self, placeholder_text="Enter preset name")
        self.entry.grid(row=1, column=0, padx=10, pady=10)

        self.button = ctk.CTkButton(self, text="Save Preset", command=self.save_preset)
        self.button.grid(row=2, column=0, padx=10, pady=10)

    def load_gestures(self):
        gestures = []
        if os.path.exists(self.gesture_csv_path):
            try:
                with open(self.gesture_csv_path, 'r', encoding='utf-8') as f:
                    reader = csv.reader(f)
                    gestures = [row[0].strip() for row in reader if row]
            except Exception as e:
                messagebox.showerror("Error", f"Could not load gestures:\n{e}")
        return gestures if gestures else ["No gestures found"]

    def create_widgets(self):
        title = ctk.CTkLabel(self, text="Create New Preset", font=("Segoe UI", 32, "bold"))
        title.pack(pady=20)
        
        dropdown_label = ctk.CTkLabel(self, text="Select Gesture:", font=("Segoe UI", 16))
        dropdown_label.pack(pady=5)
        
        self.dropdown = ctk.CTkOptionMenu(self, values=self.gesture_list, variable=self.selected_gesture)
        self.dropdown.pack(pady=5)
    
        
    def save_preset(self):
        preset_name = self.entry.get()
        print(f"Preset '{preset_name}' saved!")  # Replace with actual save logic