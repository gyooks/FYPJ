# GWBHands.py
import customtkinter as ctk
from settings import SettingsPage  # Import SettingsPage class
from change_preset import ChangePreset  # Import ChangePreset class

# Create root window
root = ctk.CTk()
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# Set the title and size of the window
root.title("GWBHands")
root.geometry("1280x720")

# Variables
current_preset_text = ctk.StringVar(value="Preset Used: None")

# Create main menu frame
mainmenu = ctk.CTkFrame(root, width=1280, height=720, fg_color="transparent")
mainmenu.place(relx=0.5, rely=0.5, anchor="center")

# App title
title = ctk.CTkLabel(mainmenu, text="GWBHands", font=("Segoe UI", 32, "bold"))
title.pack(pady=20)


# Logic to switch frames
def show_mainmenu():
    settings_frame.place_forget()
    mainmenu.place(relx=0.5, rely=0.5, anchor="center")

def show_settings():
    mainmenu.place_forget()
    settings_frame.place(relx=0.5, rely=0.5, anchor="center")
    
def show_changepreset():
    mainmenu.place_forget()
    settings_frame.place_forget()
    change_preset_frame.place(relx=0.5, rely=0.5, anchor="center")

def update_current_preset(preset_name):
    current_preset_text.set(f"Preset Used: {preset_name}")


# Buttons
button_font = ("Segoe UI", 16)
button_width = 300
button_height = 40

btn_start = ctk.CTkButton(mainmenu, text="Start", font=button_font, width=button_width, height=button_height)
btn_start.pack(pady=10)

btn_preset = ctk.CTkButton(mainmenu, textvariable=current_preset_text , font=button_font, width=button_width, state="disabled")
btn_preset.pack(pady=10)

btn_changepreset = ctk.CTkButton(mainmenu, text="Change Preset", font=button_font, width=button_width, height=button_height, command=show_changepreset)
btn_changepreset.pack(pady=10)

btn_gestures = ctk.CTkButton(mainmenu, text="Gestures", font=button_font, width=button_width, height=button_height)
btn_gestures.pack(pady=10)

btn_tutorial = ctk.CTkButton(mainmenu, text="How To Use", font=button_font, width=button_width, height=button_height)
btn_tutorial.pack(pady=10)

btn_settings = ctk.CTkButton(mainmenu, text="Settings", font=button_font, width=button_width, height=button_height, command=show_settings)
btn_settings.pack(pady=10)

btn_exit = ctk.CTkButton(mainmenu, text="Exit", font=button_font, width=button_width, height=button_height, command=root.quit)
btn_exit.pack(pady=10)

# Create settings frame but hidden until settings are accessed
settings_frame = SettingsPage(root, back_to_main_callback=show_mainmenu, width=1600, height=900, fg_color="transparent")
settings_frame.place_forget()

# Create change preset frame but hidden until accessed
change_preset_frame = ChangePreset(root, back_to_main_callback=show_mainmenu, width=1600, height=900, fg_color="transparent")
change_preset_frame.place_forget()

# Start the GUI loop
root.mainloop()