import customtkinter as ctk
from tkinter import Canvas
from PIL import Image
from customtkinter import CTkImage

class HowtousePage(ctk.CTkFrame): 
    def __init__(self, master, back_to_main_callback, **kwargs):
        super().__init__(master, **kwargs)
        self.back_to_main_callback = back_to_main_callback

        # Main title – very little padding, top-aligned
        title = ctk.CTkLabel(self, text="Tutorial", font=("Segoe UI", 60, "bold"))
        title.pack(pady=(5, 0))  # Minimized top padding

        # Main container for layout – don't expand so content stays at top
        main_container = ctk.CTkFrame(self, fg_color="transparent")
        main_container.pack(fill="x", padx=40, pady=0)  # No vertical padding

        # Left panel – also no expansion, just content
        self.left_panel = ctk.CTkFrame(main_container, fg_color="transparent")
        self.left_panel.pack(side="left", padx=(0, 40))  # No vertical fill

        # Load and display the image – no padding
        image_path = "gui/How-To-Use.jpg"
        image = CTkImage(light_image=Image.open(image_path), size=(500, 500))
        image_label = ctk.CTkLabel(self.left_panel, image=image, text="")
        image_label.pack(pady=0)  # No vertical padding

        # Add Back button
        back_button = ctk.CTkButton(self.left_panel, text="Back", command=self.cancel_and_return)
        back_button.pack(pady=(10, 0))  # Add spacing above if needed

    def cancel_and_return(self):
        self.back_to_main_callback()
        