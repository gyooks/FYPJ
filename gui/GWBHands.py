import customtkinter as ctk
import sys
import subprocess
import tkinter.messagebox as msgbox
from settings import SettingsPage  # Import SettingsPage class
from change_preset import ChangePreset  # Import ChangePreset class
from how_to_use import HowtousePage  # Import HowtousePage class
from gestures import Gestures  # Import Gestures class


# Create root window
root = ctk.CTk()
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# Set the title and size of the window
root.title("GWBHands")
root.geometry("1280x720")

# Variables
current_preset = ctk.StringVar(value="Preset Used: None")
selected_preset = None


# Create main menu frame
mainmenu = ctk.CTkFrame(root, width=1280, height=720, fg_color="transparent")
mainmenu.place(relx=0.5, rely=0.5, anchor="center")

# App title
title = ctk.CTkLabel(mainmenu, text="GWBHands", font=("Segoe UI", 32, "bold"))
title.pack(pady=20)


# Logic to switch frames
def show_mainmenu():
    settings_frame.place_forget()
    how_to_use_frame.place_forget()
    mainmenu.place(relx=0.5, rely=0.5, anchor="center")

def show_settings():
    mainmenu.place_forget()
    settings_frame.place(relx=0.5, rely=0.5, anchor="center")
    
def show_changepreset():
    mainmenu.place_forget()
    settings_frame.place_forget()
    change_preset_frame.place(relx=0.5, rely=0.5, anchor="center")

def show_howtouse():
    mainmenu.place_forget()
    how_to_use_frame.place(relx=0.5, rely=0.5, anchor="center")


def update_current_preset(preset_name):
    global selected_preset
    selected_preset = preset_name
    current_preset.set(f"Preset Used: {preset_name}")
    
#function for start button
def start_gesture_app():
    if not selected_preset:
        msgbox.showwarning("No Preset Selected", "Please select a preset before starting.")
        return
    python_executable = sys.executable # Get the current Python executable path
    
    print(f"Launching start.py with preset: {selected_preset}")
    subprocess.Popen([python_executable, "start.py", selected_preset])


# Buttons
button_font = ("Segoe UI", 16)
button_width = 300
button_height = 40

btn_start = ctk.CTkButton(mainmenu, text="Start", font=button_font, width=button_width, height=button_height, command=start_gesture_app)
btn_start.pack(pady=10)

btn_preset = ctk.CTkButton(mainmenu, textvariable= current_preset, font=button_font, width=button_width, state="disabled")
btn_preset.pack(pady=10)

btn_changepreset = ctk.CTkButton(mainmenu, text="Change Preset", font=button_font, width=button_width, height=button_height, command=show_changepreset)
btn_changepreset.pack(pady=10)

btn_gestures = ctk.CTkButton(mainmenu, text="Gestures", font=button_font, width=button_width, height=button_height)
btn_gestures.pack(pady=10)

btn_tutorial = ctk.CTkButton(mainmenu, text="How To Use", font=button_font, width=button_width, height=button_height, command=show_howtouse)
btn_tutorial.pack(pady=10)

btn_settings = ctk.CTkButton(mainmenu, text="Settings", font=button_font, width=button_width, height=button_height, command=show_settings)
btn_settings.pack(pady=10)

btn_exit = ctk.CTkButton(mainmenu, text="Exit", font=button_font, width=button_width, height=button_height, command=root.quit)
btn_exit.pack(pady=10)

# Create settings frame but hidden until settings are accessed
settings_frame = SettingsPage(root, back_to_main_callback=show_mainmenu, width=1600, height=900, fg_color="transparent")
settings_frame.place_forget()

# Create change preset frame but hidden until accessed
change_preset_frame = ChangePreset(root, update_preset_callback=update_current_preset, back_to_main_callback=show_mainmenu, width=1600, height=900, fg_color="transparent")
change_preset_frame.place_forget()

# Create Howtouse frame but hidden until accessed
how_to_use_frame = HowtousePage(root, back_to_main_callback=show_mainmenu, width=1600, height=900, fg_color="transparent")
how_to_use_frame.place_forget()

# Create Gestures frame but hidden until accessed
gestures_frame = Gestures(root, back_to_main_callback=show_mainmenu, selected_gesture=None, update_gesture_callback=update_current_preset)
gestures_frame.place_forget()

# Start the GUI loop
root.mainloop()