import customtkinter as ctk
from edit_preset import EditPreset
from create_preset import CreatePreset
import json
import os

class ChangePreset(ctk.CTkFrame):
    def __init__(self, master, back_to_main_callback, selected_preset=None, update_preset_callback=None, **kwargs):
        super().__init__(master, **kwargs)
        self.back_to_main_callback = back_to_main_callback
        self.update_preset_callback = update_preset_callback
        self.selected_preset = selected_preset

        # Load presets
        preset_base_dir = os.path.join(os.getcwd(), "gui", "presets")
        self.presets_dict = {}

        if os.path.exists(preset_base_dir):
            for folder_name in os.listdir(preset_base_dir):
                folder_path = os.path.join(preset_base_dir, folder_name)
                if os.path.isdir(folder_path):
                    mapping_file = os.path.join(folder_path, "mapping.json")
                    if os.path.exists(mapping_file):
                        try:
                            with open(mapping_file, "r") as f:
                                self.presets_dict[folder_name] = json.load(f)
                        except json.JSONDecodeError:
                            print(f"⚠️ Invalid JSON in: {mapping_file}")
        else:
            print("⚠️ Presets folder not found:", preset_base_dir)

        self.presets = list(self.presets_dict.keys())

        self.edit_preset_frame = EditPreset(
            master=master,
            preset_name="",
            preset_dir=os.path.join(os.getcwd(), "gui", "presets"),
            back_callback=self.back_from_edit,
            update_callback=self.update_preset_callback,
            width=1600,
            height=900,
            fg_color="transparent"
        )   

        self.create_widgets()

    def create_widgets(self):
        font_ui = "Segoe UI"
        button_font = (font_ui, 16)

        title = ctk.CTkLabel(self, text="Change Preset", font=(font_ui, 32, "bold"))
        title.pack(pady=20)

        subtitle = ctk.CTkLabel(self, text="Select Preset:", font=(font_ui, 24, "bold"))
        subtitle.pack(pady=10)

        preset_frame = ctk.CTkFrame(self, fg_color="transparent")
        preset_frame.pack(pady=10)

        for i, preset in enumerate(self.presets):
            ctk.CTkLabel(preset_frame, text=preset, font=(font_ui, 16, "bold")).grid(row=i, column=0, padx=10, pady=5)

            ctk.CTkButton(preset_frame, text="Use", font=button_font, width=60,
                          command=lambda p=preset: self.use_preset(p)).grid(row=i, column=1, padx=5)

            ctk.CTkButton(preset_frame, text="Delete", font=button_font, width=60,
                          command=lambda p=preset: self.delete_preset(p)).grid(row=i, column=2, padx=5)

            ctk.CTkButton(preset_frame, text="Edit", font=button_font, width=60,
                          command=lambda p=preset: self.edit_preset_window(p)).grid(row=i, column=3, padx=5)

        ctk.CTkButton(self, text="Create new preset", font=button_font, width=250, command=self.create_new_preset).pack(pady=10)
        ctk.CTkButton(self, text="Back", font=button_font, width=250, command=self.close_and_return).pack(pady=10)

    def use_preset(self, preset_name):
        preset_base = os.path.join(os.getcwd(), "gui", "presets", preset_name)
        preset_paths = {
            "mapping_path": os.path.join(preset_base, "mapping.json"),
            "keypoint_csv_path": os.path.join(preset_base, "keypoint.csv"),
            "label_csv_path": os.path.join(preset_base, "keypoint_classifier_label.csv"),
            "point_history_csv_path": os.path.join(preset_base, "point_history.csv")
        }

        print("✅ Sending preset paths to GWBHands.py:", preset_paths)
        if self.update_preset_callback:
            self.update_preset_callback(preset_name, preset_paths)
        self.close_and_return()

    def delete_preset(self, preset_name):
        print(f"Deleting preset: {preset_name}")
        if preset_name in self.presets:
            self.presets.remove(preset_name)
            self.refresh_preset_list()

    def edit_preset_window(self, preset):
        
        self.pack_forget()
    
        # Destroy previous EditPreset frame if it exists
        if hasattr(self, "edit_preset_frame") and self.edit_preset_frame is not None:
            self.edit_preset_frame.destroy()
    
        # Define callback to go back
        def back_to_change_preset():
            self.edit_preset_frame.pack_forget()
            self.edit_preset_frame.destroy()
            self.edit_preset_frame = None
            self.pack()
    
        # Instantiate new EditPreset frame
        self.edit_preset_frame = EditPreset(
            master=self.master,
            preset_name=preset,
            preset_dir=os.path.join(os.getcwd(), "gui", "presets"),
            back_callback=back_to_change_preset,
            update_callback=self.refresh_preset_list,
            width=1280,
            height=720,
            fg_color="transparent"
        )
    
        self.edit_preset_frame.pack(fill="both", expand=True)
    
    def create_new_preset(self):
        print("Creating new preset...")
        self.place_forget()
        self.create_preset_frame = CreatePreset(
            master=self.master,
            gesture_csv_path=os.path.join(os.getcwd(), "keypoint_classifier_label.csv"),
            save_dir=os.path.join(os.getcwd(), "gui", "presets"),  # ✅ Correct argument for CreatePreset
            back_callback=self.return_from_create,
            width=1600,
            height=900,
            fg_color="transparent"
            
        )
        self.create_preset_frame.place(relx=0.5, rely=0.5, anchor="center")
        
        #for debugging
        print("Current Working Directory:", os.getcwd())
        print("CSV Path:", os.path.join(os.getcwd(), "keypoint_classifier_label.csv"))
        print("Exists:", os.path.exists(os.path.join(os.getcwd(), "keypoint_classifier_label.csv")))

    def back_from_edit(self):
        self.edit_preset_frame.place_forget()
        self.place(relx=0.5, rely=0.5, anchor="center")

    def close_and_return(self):
        self.back_to_main_callback()
        self.place_forget()

    def refresh_preset_list(self):
        for widget in self.winfo_children():
            widget.destroy()
        self.create_widgets()

    def return_from_create(self):
        if hasattr(self, "create_preset_frame"):
            self.create_preset_frame.place_forget()
        self.place(relx=0.5, rely=0.5, anchor="center")
