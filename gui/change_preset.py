import customtkinter as ctk
class ChangePreset(ctk.CTkToplevel):
    def __init__(self, master):
        super().__init__(master)
        
    def create_widgets(self):
        font_ui = "Segoe UI"
        
        # Title
        title = ctk.CTkLabel(self, text="Change Preset", font=(font_ui, 32, "bold"))
        title.pack(pady=20)

        # Presets
        presets = ["Preset 1", "Preset 2", "Preset 3"]
        self.preset = []
        self.selected_index = None
        self.create_widgets()
        
        preset_frame = ctk.CTkFrame(self, fg_color="transparent")
        preset_frame.pack(pady=10)

