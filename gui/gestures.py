import customtkinter as ctk
import tkinter.messagebox as messagebox
import csv
import os

class Gestures(ctk.CTkFrame):
    def __init__(self, master, back_to_main_callback, selected_preset=None, selected_gesture=None, update_gesture_callback=None, create_gesture_callback=None, **kwargs):
        super().__init__(master, **kwargs)
        self.selected_preset = selected_preset
        self.selected_gesture = selected_gesture
        self.back_to_main_callback = back_to_main_callback
        self.update_gesture_callback = update_gesture_callback
        self.create_gesture_callback = create_gesture_callback

        # Load gestures from mapping_path
        self.gesture = self.load_gestures_from_csv()
        self.create_widgets()

    def load_gestures_from_csv(self):
        gestures = []
        if self.selected_preset and "mapping_path" in self.selected_preset:
            mapping_path = self.selected_preset["mapping_path"]
            if os.path.exists(mapping_path):
                try:
                    with open(mapping_path, 'r', encoding='utf-8') as f:
                        reader = csv.reader(f)
                        gestures = [row[0] for row in reader if row]  # Skip empty rows
                except Exception as e:
                    print(f"❌ Failed to read gesture names from CSV: {e}")
                    messagebox.showerror("CSV Error", f"Failed to load gesture names:\n{e}")
            else:
                print("❌ mapping_path does not exist:", mapping_path)
                messagebox.showerror("Missing File", f"Could not find gesture label file:\n{mapping_path}")
        else:
            print("❌ No valid selected_preset or mapping_path")
        return gestures if gestures else ["No gestures found"]

    def create_widgets(self):
        font_ui = "Segoe UI"
        button_font = (font_ui, 16)

        title = ctk.CTkLabel(self, text="Gestures", font=(font_ui, 32, "bold"))
        title.pack(pady=20)

        subtitle = ctk.CTkLabel(self, text="Select Gesture:", font=(font_ui, 24, "bold"))
        subtitle.pack(pady=10)

        gesture_frame = ctk.CTkFrame(self, fg_color="transparent")
        gesture_frame.pack(pady=10)

        self.gesture_rows = []

        for i, gesture in enumerate(self.gesture):
            gesture_label = ctk.CTkLabel(gesture_frame, text=gesture, font=(font_ui, 16, "bold"))
            gesture_label.grid(row=i, column=0, padx=10, pady=5)

            del_btn = ctk.CTkButton(gesture_frame, text="Delete", font=button_font, width=60, command=lambda p=gesture: self.delete_gesture(p))
            del_btn.grid(row=i, column=2, padx=5)

            edit_btn = ctk.CTkButton(gesture_frame, text="Rename", font=button_font, width=60, command=lambda p=gesture: self.edit_gesture(p))
            edit_btn.grid(row=i, column=3, padx=5)

        create_btn = ctk.CTkButton(self, text="Create new gesture", font=button_font, width=250,
                                   command=self.create_gesture_callback if self.create_gesture_callback else self.create_new_gesture)
        create_btn.pack(pady=10)

        back_btn = ctk.CTkButton(self, text="Back", font=button_font, width=250, command=self.close_and_return)
        back_btn.pack(pady=10)

    def delete_gesture(self, gesture_name):
        print(f"Deleting gesture: {gesture_name}")
        if gesture_name in self.gesture:
            self.gesture.remove(gesture_name)
            self.refresh_gesture_list()

    def edit_gesture(self, gesture_name):
        print(f"Renaming gesture: {gesture_name}")
        # TODO: Add rename logic

    def create_new_gesture(self):
        if not self.selected_preset:
            messagebox.showwarning("Preset Required", "Please select a preset before creating a new gesture.")
            return
        if self.create_gesture_callback:
            self.create_gesture_callback()

    def close_and_return(self):
        self.place_forget()
        self.back_to_main_callback()

    def refresh_gesture_list(self):
        for widget in self.winfo_children():
            widget.destroy()
        self.gesture = self.load_gestures_from_csv()
        self.create_widgets()