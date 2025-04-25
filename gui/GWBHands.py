import customtkinter as ctk
from customtkinter import *

#create root window
root = ctk.CTk()
ctk.set_appearance_mode("dark") 
ctk.set_default_color_theme("blue")

# Set the title and size of the window
root.title("GWBHands")
root.geometry("1280x720")

# Create a frame to hold the widgets
center = ctk.CTkFrame(root, width=1600, height=900, fg_color="transparent")
center.place(relx=0.5, rely=0.5, anchor="center")

#App title
title = ctk.CTkLabel(root, text="GWBHands", font=("Segoe UI", 32, "bold"))
title.pack(pady=20)
title.place(relx=0.5, rely=0.1, anchor="center")

#Buttons
button_font = ("Segoe UI", 16)
button_width = 240
button_height = 50

btn_start = ctk.CTkButton(center, text="Start", font=button_font, width=button_width, height=button_height)
btn_start.pack(pady=10)

btn_preset = ctk.CTkButton(center, text="Preset Used: ", font=button_font, width=button_width, state="disabled")
btn_preset.pack(pady=10)

btn_changepreset = ctk.CTkButton(center, text="Change Preset", font=button_font, width=button_width, height=button_height)
btn_changepreset.pack(pady=10)

btn_settings = ctk.CTkButton(center, text="Settings", font=button_font, width=button_width, height=button_height)
btn_settings.pack(pady=10)

btn_exit = ctk.CTkButton(center, text="Exit", font=button_font, width=button_width, height=button_height, command=root.quit)
btn_exit.pack(pady=10)


#execute GUI
root.mainloop()
