import customtkinter as ctk
import os
from tkinter import Canvas
from PIL import Image
from customtkinter import CTkImage

class HowtousePage(ctk.CTkFrame): 
    def __init__(self, master, back_to_main_callback, **kwargs):
        super().__init__(master, **kwargs)
        self.back_to_main_callback = back_to_main_callback
        
        # Title
        title = ctk.CTkLabel(self, text="Tutorial", font=("Segoe UI", 60, "bold"))
        title.pack(pady=(5, 0))

        # Main container
        main_container = ctk.CTkFrame(self, fg_color="transparent")
        main_container.pack(fill="both", expand=True, padx=40, pady=0)

        # Left panel for image & back button
        self.left_panel = ctk.CTkFrame(main_container, fg_color="transparent")
        self.left_panel.pack(side="left", padx=(0, 40), fill="both", expand=True)

        # Image loading
        base_dir = os.path.dirname(os.path.abspath(__file__))
        image_path = os.path.join(base_dir, "assets", "How-To-Use.jpg")

        if os.path.exists(image_path):
            # Load original
            img = Image.open(image_path)

            # Maximum display size
            max_width, max_height = 800, 800  # tweak for your layout

            # Resize keeping aspect ratio
            img.thumbnail((max_width, max_height), Image.LANCZOS)

            # Create CTkImage with resized dimensions
            image = CTkImage(light_image=img, size=img.size)

            # Add image to label
            image_label = ctk.CTkLabel(self.left_panel, image=image, text="")
            image_label.pack(pady=0)
        else:
            print(f"[ERROR] Image not found at: {image_path}")

        # Back button
        back_button = ctk.CTkButton(self.left_panel, text="Back", command=self.cancel_and_return)
        back_button.pack(pady=(10, 0))

    def cancel_and_return(self):
        self.back_to_main_callback()