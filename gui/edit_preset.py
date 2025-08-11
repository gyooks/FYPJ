import customtkinter as ctk
import os
import json
import csv
import tkinter.messagebox as messagebox

font_family = "Segoe UI"

class EditPreset(ctk.CTkFrame):
    def __init__(self, master, preset_name, preset_dir, back_callback, update_callback, **kwargs):
        super().__init__(master, **kwargs)
        self.preset_name = preset_name
        self.preset_dir = preset_dir
        self.mapping_rows = []
        self.back_callback = back_callback
        self.update_callback = update_callback
        self.mapping_json_path = os.path.join(preset_dir, preset_name, "mapping.json")
        self.label_csv_path = os.path.join(preset_dir, preset_name, "keypoint_classifier_label.csv")

        self.gesture_options = self.load_gestures()
        self.gesture_mapping = self.load_existing_mapping()

        # Title
        ctk.CTkLabel(self, text=f"Edit Preset: {preset_name}", font=(font_family, 20, "bold")).pack(pady=(10, 20))

        # Mapping container
        self.mapping_container = ctk.CTkFrame(self, fg_color="transparent")
        self.mapping_container.pack(pady=(5, 10))

        # Existing rows
        for gesture, key in self.gesture_mapping.items():
            self.add_mapping_row(initial_gesture=gesture, initial_key=key)


        # Button to add & delete row
        row_frame = ctk.CTkFrame(self, fg_color="transparent")
        row_frame.pack(pady=(10, 10))

        ctk.CTkButton(row_frame, text="+ Add Row", command=self.add_mapping_row).pack(side="left", padx=5)
        ctk.CTkButton(row_frame, text="− Delete Row", command=self.delete_last_row).pack(side="left", padx=5)
    
        # Confirm/Cancel Buttons
        button_frame = ctk.CTkFrame(self, fg_color="transparent")
        button_frame.pack(pady=(20, 10))
        ctk.CTkButton(button_frame, text="Save Changes", command=self.save_changes).pack(side="left", padx=10)
        ctk.CTkButton(button_frame, text="Cancel", command=self.cancel_and_close).pack(side="left", padx=10)

    def load_gestures(self):
        if not os.path.exists(self.label_csv_path):
            return []

        gestures = []
        with open(self.label_csv_path, newline='', encoding='utf-8-sig') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                if row:
                    gestures.append(row[0].strip().lstrip("\ufeff"))  # strip BOM if present
        return sorted(list(set(gestures)))


    def load_existing_mapping(self):
        if not os.path.exists(self.mapping_json_path):
            return {}
        with open(self.mapping_json_path, 'r', encoding='utf-8-sig') as f:
            data = json.load(f)
            return {k.lstrip("\ufeff"): v for k, v in data.items()}


    def add_mapping_row(self, initial_gesture="", initial_key=""):
        row_frame = ctk.CTkFrame(self.mapping_container, fg_color="transparent")
        row_frame.pack(pady=5)

        gesture_var = ctk.StringVar(
            value=initial_gesture if initial_gesture else self.gesture_options[0] if self.gesture_options else ""
        )
        key_var = ctk.StringVar(value=initial_key)

        # Gesture selection
        gesture_menu = ctk.CTkOptionMenu(row_frame, variable=gesture_var, values=self.gesture_options, width=150)
        gesture_menu.pack(side="left", padx=5)

        # Label
        ctk.CTkLabel(row_frame, text="Key:", font=(font_family, 12)).pack(side="left", padx=5)

        # Disabled entry for showing current binding
        key_entry = ctk.CTkEntry(row_frame, textvariable=key_var, width=100, state="disabled")
        key_entry.pack(side="left", padx=5)

        # Bind button
        bind_btn = ctk.CTkButton(row_frame, text="Bind", width=50)
        bind_btn.pack(side="left", padx=5)


        state = {"capturing": False}

        def start_capture():
            key_var.set("...waiting for input...")
            state["capturing"] = True
            self.master.bind_all("<Key>", capture_key)
            self.master.bind_all("<Button>", capture_mouse)

        def stop_capture():
            state["capturing"] = False
            self.master.unbind_all("<Key>")
            self.master.unbind_all("<Button>")

        def capture_key(event):
            if state["capturing"]:
                key_var.set(event.keysym)
                stop_capture()

        def capture_mouse(event):
            if state["capturing"]:
                if event.num == 1:
                    key_var.set("left_click")
                elif event.num == 3:
                    key_var.set("right_click")
                else:
                    key_var.set(f"mouse_button_{event.num}")
                stop_capture()

        bind_btn.configure(command=start_capture)

        # Keep reference so save_changes() will work
        self.mapping_rows.append((gesture_var, key_var, row_frame))

    def delete_last_row(self):
        if self.mapping_rows:
            gesture_var, key_var, row_frame = self.mapping_rows.pop()
            try:
                row_frame.destroy()
            except Exception:
                pass
        else:
            messagebox.showwarning("Warning", "No rows to delete.")
            
    def save_changes(self):
        updated_mapping = {}

        for gesture_var, key_var, _ in self.mapping_rows:  
            gesture = gesture_var.get().strip()
            key = key_var.get().strip()
            if gesture and key:
                updated_mapping[gesture] = key

        if not updated_mapping:
            messagebox.showerror("Error", "At least one gesture-to-key mapping must be provided.")
            return

        try:
            with open(self.mapping_json_path, "w", encoding="utf-8-sig") as f:
                json.dump(updated_mapping, f, indent=4)

            messagebox.showinfo("Success", "Preset updated successfully.")
            if self.update_callback:
                self.update_callback()
            self.back_callback()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save changes: {str(e)}")

    def cancel_and_close(self):
        self.back_callback()

