import customtkinter as ctk
import os
import csv
import json
import tkinter.messagebox as messagebox
import shutil

font_family = "Segoe UI"
class CreatePreset(ctk.CTkFrame):
    def __init__(self, master, gesture_csv_path, save_dir, back_callback,update_presets_callback, **kwargs):
        super().__init__(master, **kwargs)
        self.gesture_csv_path = gesture_csv_path
        self.save_dir = save_dir
        self.update_presets_callback = update_presets_callback
        self.back_callback = back_callback
        self.mapping_rows = []
        self.gesture_options = self.load_gestures()
        self.preset_name = ctk.StringVar()

        # Title
        ctk.CTkLabel(self, text="Create new preset", font=(font_family, 20, "bold")).pack(pady=(10, 20))

        # Preset Name Row
        preset_frame = ctk.CTkFrame(self, fg_color="transparent")
        preset_frame.pack(pady=(0, 10))
        ctk.CTkLabel(preset_frame, text="Preset Name:", font=(font_family, 14)).pack(side="left")
        ctk.CTkEntry(preset_frame, textvariable=self.preset_name, width=150).pack(side="left", padx=10)
        ctk.CTkButton(preset_frame, text="+", width=30, command=self.add_mapping_row).pack(side="left")

        # Container for gesture–key mapping rows
        self.mapping_container = ctk.CTkFrame(self, fg_color="transparent")
        self.mapping_container.pack(pady=(5, 10))
        self.add_mapping_row()  # Add first row by default

        # Confirm/Cancel Buttons
        button_frame = ctk.CTkFrame(self, fg_color="transparent")
        button_frame.pack(pady=(20, 10))

        ctk.CTkButton(button_frame, text="Confirm", command=self.save_preset).pack(side="left", padx=10)
        ctk.CTkButton(button_frame, text="Cancel", command=self.cancel_and_close).pack(side="left", padx=10)

    
    def load_gestures(self):
        gestures = set()
        presets_path = self.save_dir
    
        if os.path.exists(presets_path):
            for folder_name in os.listdir(presets_path):
                folder_path = os.path.join(presets_path, folder_name)
                if os.path.isdir(folder_path):
                    label_csv = os.path.join(folder_path, "keypoint_classifier_label.csv")
                    if os.path.exists(label_csv):
                        with open(label_csv, newline='', encoding='utf-8') as csvfile:
                            reader = csv.reader(csvfile)
                            for row in reader:
                                if row:
                                    gestures.add(row[0].strip())
    
        return sorted(list(gestures))

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
        
    def add_mapping_row(self):
        row_frame = ctk.CTkFrame(self.mapping_container, fg_color="transparent")
        row_frame.pack(pady=5)  
        
        gesture_var = ctk.StringVar(value=self.gesture_options[0] if self.gesture_options else "")
        key_var = ctk.StringVar()   
        
        gesture_menu = ctk.CTkOptionMenu(row_frame, variable=gesture_var, values=self.gesture_options, width=150)
        gesture_menu.pack(side="left", padx=5)
        
        ctk.CTkLabel(row_frame, text="Key Mapped:", font=(font_family, 12)).pack(side="left", padx=5)
        key_entry = ctk.CTkEntry(row_frame, textvariable=key_var, width=100)
        key_entry.pack(side="left", padx=5) 
        self.mapping_rows.append((gesture_var, key_var))

    def update_mapping_display(self):
        mapping_text = "\n".join([f"{gesture}: {key}" for gesture, key in self.gesture_key_mapping.items()])
        self.mapping_display.configure(text=mapping_text)

    def cancel_and_close(self):
        self.place_forget()
        self.back_callback()

    def save_preset(self):
        name = self.preset_name.get().strip()
        if not name:
            messagebox.showerror("Error", "Preset name cannot be empty.")
            return

        gesture_to_key = {}

        for gesture_var, key_var in self.mapping_rows:
            gesture = gesture_var.get().strip()
            key = key_var.get().strip()
            if not gesture or not key:
                continue
            gesture_to_key[gesture] = key

        if not gesture_to_key:
            messagebox.showerror("Error", "No valid gesture mappings.")
            return

        # Create new preset folder
        preset_folder = os.path.join(self.save_dir, name)
        if os.path.exists(preset_folder):
            messagebox.showerror("Error", f"A preset named '{name}' already exists.")
            return

        os.makedirs(preset_folder)

        try:
            
            default_folder = os.path.join(self.save_dir, "Default")

            required_files = [
                "keypoint_classifier_label.csv",
                "keypoint.csv",
                "mapping.json",  
                "point_history.csv",
                "point_history_classifier_label.csv"
            ]

            # ✅ Copy files from Default to new preset
            for filename in required_files:
                src = os.path.join(default_folder, filename)
                dst = os.path.join(preset_folder, filename)

                if not os.path.exists(src):
                    messagebox.showerror("Error", f"Missing default file: {filename}")
                    return

                shutil.copy2(src, dst)

            # ✅ Overwrite mapping.json with user-defined gesture→key mapping
            mapping_path = os.path.join(preset_folder, "mapping.json")
            with open(mapping_path, "w", encoding="utf-8") as jsonfile:
                json.dump(gesture_to_key, jsonfile, indent=4)

            messagebox.showinfo("Success", f"Preset '{name}' created successfully.")
            
            if self.refresh_callback:
                self.refresh_callback()
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to create preset: {str(e)}")
