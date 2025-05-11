import customtkinter as ctk
class ChangePreset(ctk.CTkToplevel):
    def __init__(self, master, back_to_main_callback,selected_preset=None, update_preset_callback=None, **kwargs):
        super().__init__(master, **kwargs)
        self.title("Change Preset")
        self.selected_preset = selected_preset
        self.back_to_main_callback = back_to_main_callback
        self.update_preset_callback = update_preset_callback
        self.create_widgets()
        
    def create_widgets(self):
        font_ui = "Segoe UI"
        button_font = (font_ui, 16)
        
        # Title
        title = ctk.CTkLabel(self, text="Change Preset", font=(font_ui, 32, "bold"))
        title.pack(pady=20)

        # Presets
        self.presets = ["Preset 1", "Preset 2", "Preset 3"]
        
        title = ctk.CTkLabel(self, text="Select Preset:", font=(font_ui, 32, "bold"))
        title.pack(pady=20)
        
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

            back_btn = ctk.CTkButton(self, text="Back", font=button_font, width=250, command=self.destroy)
            back_btn.pack(pady=10)
            
    def use_preset(self, preset_name):
    # Logic to use the selected preset
        print(f"Using preset: {preset_name}")
        if self.selected_preset:
            self.selected_preset.set(preset_name)
        self.destroy()
        
    def delete_preset(self, preset_name):
        # Logic to delete the selected preset
        print(f"Deleting preset: {preset_name}")
        self.presets.remove(preset_name)
        self.preset_rows()
        