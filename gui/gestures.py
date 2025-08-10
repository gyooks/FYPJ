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
        if self.selected_preset and "label_csv_path" in self.selected_preset:
            label_csv_path = self.selected_preset["label_csv_path"]
            if os.path.exists(label_csv_path):
                try:
                    with open(label_csv_path, 'r', encoding='utf-8') as f:
                        reader = csv.reader(f)
                        # Read first column, strip whitespace
                        gestures = [row[0].strip() for row in reader if row] 
                except Exception as e:
                    print(f"Failed to read gesture names from CSV: {e}")
                    messagebox.showerror("CSV Error", f"Failed to load gesture names:\n{e}")
            else:
                print("label_csv_path does not exist:", label_csv_path)
                messagebox.showerror("Missing File", f"Could not find gesture label file:\n{label_csv_path}")
        else:
            print("No valid selected_preset or label_csv_path")
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
        if gesture_name not in self.gesture:
            return

        confirm = messagebox.askyesno("Confirm Delete", f"Delete gesture '{gesture_name}'?")
        if not confirm:
            return

        gesture_index = self.gesture.index(gesture_name)
        self.gesture.remove(gesture_name)

        try:
            with open(self.selected_preset["label_csv_path"], "w", newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                for g in self.gesture:
                    writer.writerow([g])
        except Exception as e:
            messagebox.showerror("Error", f"Failed to update label CSV:\n{e}")
            return

        # Actually perform deletion from keypoint.csv
        self.remove_rows_by_gesture_id(gesture_index)
        self.refresh_gesture_list()


    def remove_rows_by_gesture_id(self, gesture_index):
        keypoint_csv_path = self.selected_preset.get("keypoint_csv_path")

        if not keypoint_csv_path or not os.path.exists(keypoint_csv_path):
            print("keypoint.csv not found at:", keypoint_csv_path)
            return

        try:
            with open(keypoint_csv_path, "r", encoding="utf-8") as f:
                rows = list(csv.reader(f))

            updated_rows = []
            removed_count = 0
            reindexed_count = 0

            for row in rows:
                if not row:
                    continue
                try:
                    # handles both "2" and "2.0"
                    row_id = int(float(row[0]))
                    if row_id == gesture_index:
                        removed_count += 1
                        continue
                    elif row_id > gesture_index:
                        row[0] = str(row_id - 1)
                        reindexed_count += 1
                except ValueError:
                    print(f"Could not parse row ID: {row[0]}")
                updated_rows.append(row)

            with open(keypoint_csv_path, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerows(updated_rows)

            print(f"Removed {removed_count} rows for gesture index {gesture_index}")
            print(f"Reindexed {reindexed_count} rows after deletion")

        except Exception as e:
            messagebox.showerror("Error", f"Failed to update keypoint.csv:\n{e}")

    def edit_gesture(self, gesture_name):
        def on_rename(old_name, new_name):
            try:
                index = self.gesture.index(old_name)
                self.gesture[index] = new_name

                label_csv_path = self.selected_preset["label_csv_path"]
                with open(label_csv_path, "w", newline="", encoding='utf-8') as f:
                    writer = csv.writer(f)
                    for g in self.gesture:
                        writer.writerow([g])

                messagebox.showinfo("Success", f"Gesture '{old_name}' renamed to '{new_name}'.")
                self.refresh_gesture_list()

            except Exception as e:
                messagebox.showerror("Error", f"Failed to rename gesture:\n{e}")

        RenameGesturePopup(self, gesture_name, self.gesture, on_rename)

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


class RenameGesturePopup(ctk.CTkToplevel):
    def __init__(self, parent, current_name, existing_names, on_rename_callback):
        super().__init__(parent)
        self.title("Rename Gesture")
        self.geometry("400x200")
        self.resizable(False, False)
        self.grab_set()
        self.focus()

        self.current_name = current_name
        self.existing_names = existing_names
        self.on_rename_callback = on_rename_callback

        self.label = ctk.CTkLabel(self, text=f"Rename '{current_name}' to:", font=("Segoe UI", 18))
        self.label.pack(pady=20)

        self.entry = ctk.CTkEntry(self, width=250)
        self.entry.insert(0, current_name)
        self.entry.pack(pady=10)
        self.entry.focus()

        self.button_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.button_frame.pack(pady=10)

        self.cancel_btn = ctk.CTkButton(self.button_frame, text="Cancel", command=self.destroy, width=80)
        self.cancel_btn.grid(row=0, column=0, padx=10)

        self.confirm_btn = ctk.CTkButton(self.button_frame, text="Rename", command=self.rename, width=80)
        self.confirm_btn.grid(row=0, column=1, padx=10)

    def rename(self):
        new_name = self.entry.get().strip()
        if not new_name:
            messagebox.showwarning("Invalid Name", "Name cannot be empty.")
            return
        if new_name == self.current_name:
            self.destroy()
            return
        if new_name in self.existing_names:
            messagebox.showwarning("Duplicate Name", f"The gesture name '{new_name}' already exists.")
            return

        self.on_rename_callback(self.current_name, new_name)
        self.destroy()