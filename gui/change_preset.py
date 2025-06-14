import customtkinter as ctk
from edit_preset import EditPreset
class ChangePreset(ctk.CTkFrame):
    def __init__(self, master, back_to_main_callback, selected_preset=None, update_preset_callback=None, **kwargs):
        super().__init__(master, **kwargs)
        self.selected_preset = selected_preset
        self.back_to_main_callback = back_to_main_callback
        self.update_preset_callback = update_preset_callback
        self.presets = ["Preset 1", "Preset 2", "Preset 3"]
        self.edit_preset_frame = EditPreset(master, preset_name="", back_callback=self.back_from_edit, save_changes=self.update_preset_callback, width=1600, height=900, fg_color="transparent")
        self.edit_preset_frame.place_forget()
        self.create_widgets()
        
    def create_widgets(self):
        font_ui = "Segoe UI"
        button_font = (font_ui, 16)
        
        # Title
        title = ctk.CTkLabel(self, text="Change Preset", font=(font_ui, 32, "bold"))
        title.pack(pady=20)

        subtitle = ctk.CTkLabel(self, text="Select Preset:", font=(font_ui, 24, "bold"))
        subtitle.pack(pady=10)
        
        preset_frame = ctk.CTkFrame(self, fg_color="transparent")
        preset_frame.pack(pady=10)
        
        self.preset_rows = []

        for i, preset in enumerate(self.presets):
            preset_label = ctk.CTkLabel(preset_frame, text=preset, font=(font_ui, 16, "bold"))
            preset_label.grid(row=i, column=0, padx=10, pady=5)
            
            # Use Button
            use_btn = ctk.CTkButton(preset_frame, text="Use", font=button_font, width=60, command=lambda p=preset: self.use_preset(p))
            use_btn.grid(row=i, column=1, padx=5)
            
            del_btn = ctk.CTkButton(preset_frame, text="Delete", font=button_font, width=60, command=lambda p=preset: self.delete_preset(p))
            del_btn.grid(row=i, column=2, padx=5)

            edit_btn = ctk.CTkButton(preset_frame, text="Edit", font=button_font, width=60, command=lambda p=preset: self.edit_preset(p))
            edit_btn.grid(row=i, column=3, padx=5)
        
        create_btn = ctk.CTkButton(self, text="Create new preset", font=button_font, width=250, command=self.create_new_preset)
        create_btn.pack(pady=10)

        back_btn = ctk.CTkButton(self, text="Back", font=button_font, width=250, command=self.close_and_return)
        back_btn.pack(pady=10)
            
    def use_preset(self, preset_name):
        print(f"Using preset: {preset_name}")
        if self.update_preset_callback:
            self.update_preset_callback(preset_name)  # Notify the main GUI
        self.close_and_return()
        
    def delete_preset(self, preset_name):
        print(f"Deleting preset: {preset_name}")
        if preset_name in self.presets:
            self.presets.remove(preset_name)
            self.refresh_preset_list()
    
    def edit_preset(self, preset_name):
        self.place_forget()
        self.edit_preset_frame.preset_name = preset_name
        self.edit_preset_frame.name_entry.delete(0, "end")
        self.edit_preset_frame.name_entry.insert(0, preset_name)
        self.edit_preset_frame.title.configure(text=f"Editing: {preset_name}")
        self.edit_preset_frame.place(relx=0.5, rely=0.5, anchor="center")
        
    def back_from_edit(self):
        self.edit_preset_frame.place_forget()
        self.place(relx=0.5, rely=0.5, anchor="center")

    def create_new_preset(self):
        print("Creating new preset...")
        # Haven't implemented this functionality yet
        
    def close_and_return(self):
        self.back_to_main_callback()
        self.place_forget()
        
    def refresh_preset_list(self):
        # Clear and recreate preset UI (simplest way)
        for widget in self.winfo_children():
            widget.destroy()
        self.create_widgets()

# For testing this page alone

# if __name__ == "__main__":
#     import customtkinter as ctk

#     def dummy_callback(preset):
#         print(f"Selected preset in test mode: {preset}")

#     def back_to_main():
#         print("Returning to main (test)")

#     root = ctk.CTk()
#     root.geometry("800x600")
#     root.title("Test ChangePreset")

#     win = ChangePreset(root, back_to_main_callback=back_to_main, update_preset_callback=dummy_callback)
#     win.mainloop()
