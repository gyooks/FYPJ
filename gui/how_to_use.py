import customtkinter as ctk
import os
from tkinter import Canvas
from PIL import Image
from customtkinter import CTkImage

class HowtousePage(ctk.CTkFrame): 
    def __init__(self, master, back_to_main_callback, **kwargs):
        super().__init__(master, **kwargs)
        self.back_to_main_callback = back_to_main_callback
        
        title = ctk.CTkLabel(self, text="Tutorial", font=("Segoe UI", 60, "bold"))
        title.pack(pady=(5, 0))

        main_container = ctk.CTkFrame(self, fg_color="transparent")
        main_container.pack(fill="x", padx=40, pady=0)

        self.left_panel = ctk.CTkFrame(main_container, fg_color="transparent")
        self.left_panel.pack(side="left", padx=(0, 40))

        base_dir = os.path.dirname(os.path.abspath(__file__))
        image_path = os.path.join(base_dir, "assets", "How-To-Use.jpg")

        # Check if image exists
        if os.path.exists(image_path):
            image = CTkImage(light_image=Image.open(image_path), size=(500, 500))
        else:
            print(f"[ERROR] Image not found at: {image_path}")
            image = None

        # Only create label if image was loaded
        if image:
            image_label = ctk.CTkLabel(self.left_panel, image=image, text="")
            image_label.pack(pady=0)

        # Add Back button
        back_button = ctk.CTkButton(self.left_panel, text="Back", command=self.cancel_and_return)
        back_button.pack(pady=(10, 0))

    def cancel_and_return(self):
        self.back_to_main_callback()
        