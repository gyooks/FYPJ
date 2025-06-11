import customtkinter as ctk
from tkinter import Canvas
from PIL import Image
from customtkinter import CTkImage

class HowtousePage(ctk.CTkFrame): 
    def __init__(self, master, back_to_main_callback, **kwargs):
        super().__init__(master, **kwargs)
        self.back_to_main_callback = back_to_main_callback

        # Main title – very little padding, top-aligned
        title = ctk.CTkLabel(self, text="How To Use", font=("Segoe UI", 60, "bold"))
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



#THIS IS ANOTHER WAY OF PLACING THE BACK BUTTON (TOP RIGHT CORNER)

#import customtkinter as ctk
#from PIL import Image
#from customtkinter import CTkImage

#class HowtousePage(ctk.CTkFrame): 
#    def __init__(self, master, back_to_main_callback, **kwargs):
#        super().__init__(master, **kwargs)
#        self.back_to_main_callback = back_to_main_callback

        # Top bar frame for title and back button
#       top_bar = ctk.CTkFrame(self, fg_color="transparent")
#       top_bar.pack(fill="x", padx=40, pady=(20, 10))

        #Title label on the left in top bar
#       title = ctk.CTkLabel(top_bar, text="How To Use", font=("Segoe UI", 60, "bold"))
#       title.pack(side="left")

        #Back button on the right in top bar
#       back_button = ctk.CTkButton(top_bar, text="Back", command=self.cancel_and_return, width=80)
#       back_button.pack(side="right")

        # Main container for image below the top bar
#        main_container = ctk.CTkFrame(self, fg_color="transparent")
#        main_container.pack(fill="both", expand=True, padx=40, pady=20)

        # Load image
#        image_path = "gui/How-To-Use.jpg"
#        image = CTkImage(light_image=Image.open(image_path), size=(500, 500))

        # Image label (only image now)
#        image_label = ctk.CTkLabel(main_container, image=image, text="")
#        image_label.pack()

#    def cancel_and_return(self):
#        self.back_to_main_callback()
#


