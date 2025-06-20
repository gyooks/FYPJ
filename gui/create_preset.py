import customtkinter as ctk
import os
import csv
import json
import tkinter.messagebox as messagebox
font_family = "Segoe UI"
class CreatePreset(ctk.CTkFrame):
    def __init__(self, master, gesture_csv_path, save_preset_callback, back_callback, **kwargs):
        super().__init__(master, **kwargs)
        self.preset_name = ctk.StringVar()
        self.gesture_csv_path = gesture_csv_path
        self.save_preset_callback = save_preset_callback
        self.back_callback = back_callback
        self.gesture_list = self.load_gestures()
        self.gesture_key_mapping = {}  # {gesture: key}
        self.selected_gesture = ctk.StringVar(value=self.gesture_list[0] if self.gesture_list else "None")
        
    
        self.create_widgets()

    
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
        title = ctk.CTkLabel(self, text="Create New Preset", font=(font_family, 32, "bold"))
        title.pack(pady=20)
    
        preset_name_label = ctk.CTkLabel(self, text="Preset Name:", font=(font_family, 16))
        preset_name_label.pack(pady=5)

        self.preset_name_entry = ctk.CTkEntry(self, textvariable=self.preset_name)
        self.preset_name_entry.pack(pady=5)

        dropdown_label = ctk.CTkLabel(self, text="Select Gesture:", font=(font_family, 16))
        dropdown_label.pack(pady=5)

        self.dropdown = ctk.CTkOptionMenu(self, values=self.gesture_list, variable=self.selected_gesture)
        self.dropdown.pack(pady=5)

        key_label = ctk.CTkLabel(self, text="Enter Key to Assign:", font=(font_family, 16))
        key_label.pack(pady=5)

        self.key_entry = ctk.CTkEntry(self)
        self.key_entry.pack(pady=5)


        add_btn = ctk.CTkButton(self, text="Add to Mapping", command=self.add_mapping)
        add_btn.pack(pady=10)

        self.mapping_display = ctk.CTkLabel(self, text="", font=(font_family, 14), justify="left")
        self.mapping_display.pack(pady=10)

        save_btn = ctk.CTkButton(self, text="Save Preset", command=self.save_preset)
        save_btn.pack(pady=10)

        back_btn = ctk.CTkButton(self, text="Back", command=self.back_callback)
        back_btn.pack(pady=10)
        
    def add_mapping(self):
        gesture = self.selected_gesture.get()
        key = self.key_entry.get().strip().lower()

        if not key:
            messagebox.showwarning("Missing Input", "Please enter a key to assign.")
            return

        self.gesture_key_mapping[gesture] = key
        self.key_entry.delete(0, "end")
        self.update_mapping_display()

    def update_mapping_display(self):
        mapping_text = "\n".join([f"{gesture}: {key}" for gesture, key in self.gesture_key_mapping.items()])
        self.mapping_display.configure(text=mapping_text)

    def save_preset(self):
        if not self.gesture_key_mapping:
            messagebox.showwarning("No Mapping", "You must assign at least one gesture to a key.")
            return

        file_path = ctk.filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
        if not file_path:
            return

        try:
            with open(file_path, "w") as f:
                json.dump(self.gesture_key_mapping, f, indent=4)
            messagebox.showinfo("Saved", f"Preset saved to:\n{file_path}")
            if self.save_preset_callback:
                self.save_preset_callback(file_path, self.preset_name.get().strip())
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save preset:\n{e}")