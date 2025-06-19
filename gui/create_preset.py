import customtkinter as ctk

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

    def save_preset(self):
        preset_name = self.entry.get()
        print(f"Preset '{preset_name}' saved!")  # Replace with actual save logic