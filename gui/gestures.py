import customtkinter as ctk
import tkinter.messagebox as messagebox

class Gestures(ctk.CTkFrame):
    def __init__(self, master, back_to_main_callback, selected_preset=None, selected_gesture=None, update_gesture_callback=None, create_gesture_callback=None, **kwargs):
        super().__init__(master, **kwargs)
        self.selected_preset = selected_preset  # <-- Added here
        self.selected_gesture = selected_gesture
        self.back_to_main_callback = back_to_main_callback
        self.update_gesture_callback = update_gesture_callback
        self.create_gesture_callback = create_gesture_callback  # Save callback
        
        self.gesture = ["Gesture 1", "Gesture 2", "Gesture 3"]
        self.create_widgets()
        
    def create_widgets(self):
        font_ui = "Segoe UI"
        button_font = (font_ui, 16)
        
        # Title
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
        
        # Use the create_gesture_callback if provided, else fallback
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
        # Haven't implemented this functionality yet

    def create_new_gesture(self):
        if not self.selected_preset:
            messagebox.showwarning("Preset Required", "Please select a preset before creating a new gesture.")
            print("❌ No preset selected. Cannot create gesture.")
            return

        print("✅ Proceeding to create new gesture...")
        if self.create_gesture_callback:
            self.create_gesture_callback()
        
    def close_and_return(self):
        self.place_forget()  # Just hide it
        self.back_to_main_callback()
        
    def refresh_gesture_list(self):
        # Clear and recreate gesture UI (simplest way)
        for widget in self.winfo_children():
            widget.destroy()
        self.create_widgets()


# For testing this page alone
if __name__ == "__main__":
    import customtkinter as ctk

    def dummy_callback():
        print("Create gesture callback called")

    def dummy_back():
        print("Back called")

    root = ctk.CTk()
    root.geometry("800x600")
    root.title("Test Gestures")

    # Test without preset selected — should warn on creating gesture
    win_no_preset = Gestures(root, back_to_main_callback=dummy_back, create_gesture_callback=dummy_callback)
    win_no_preset.pack(expand=True, fill="both")

    # Uncomment below to test with preset selected — should allow creation without warning
    # win_with_preset = Gestures(root, back_to_main_callback=dummy_back, create_gesture_callback=dummy_callback, selected_preset="ExamplePreset")
    # win_with_preset.pack(expand=True, fill="both")

    root.mainloop()