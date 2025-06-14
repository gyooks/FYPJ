import customtkinter as ctk

class EditPreset(ctk.CTkFrame):
    def __init__(self, master, preset_name, back_callback, **kwargs):
        super().__init__(master, **kwargs)
        self.preset_name = preset_name
        self.back_callback = back_callback

        self.title = ctk.CTkLabel(self, text=f"Editing: {preset_name}", font=("Segoe UI", 32, "bold"))
        self.title.pack(pady=20)

        self.name_entry = ctk.CTkEntry(self, placeholder_text="Enter new name")
        self.name_entry.insert(0, preset_name)
        self.name_entry.pack(pady=10)

        save_btn = ctk.CTkButton(self, text="Save", command=self.save_changes)
        save_btn.pack(pady=10)

        back_btn = ctk.CTkButton(self, text="Back", command=self.close_page)
        back_btn.pack(pady=10)

    def save_changes(self):
        new_name = self.name_entry.get()
        print(f"Saved new name: {new_name}")  # Replace with update logic
        self.close_page()

    def close_page(self):
        self.place_forget()
        self.back_callback()