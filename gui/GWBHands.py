import customtkinter as ctk
import sys
import subprocess
import tkinter.messagebox as msgbox
import os
import nbformat
import cv2
import numpy as np
import pyautogui
import time
import pandas as pd
import threading
import csv
import json
import numpy as np
import mediapipe as mp


from nbconvert.preprocessors import ExecutePreprocessor
from settings import SettingsPage  # Import SettingsPage class
from change_preset import ChangePreset  # Import ChangePreset class
from how_to_use import HowtousePage  # Import HowtousePage class
from gestures import Gestures  # Import Gestures class
from create_gestures import CreateGestures  # Import CreateGestures class (webcam frame)
from create_preset import CreatePreset
from utils import cvfpscalc
from collections import deque
from model import KeyPointClassifier

# Get the directory where this script is running
script_dir = os.path.dirname(os.path.abspath(__file__))
notebook_path = os.path.join(script_dir, "keypoint_classification_EN.ipynb")

# Create root window
root = ctk.CTk()
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")
root.title("GWBHands")
root.geometry("1280x720")

# Variables
current_preset = ctk.StringVar(value="Preset Used: None")
selected_preset = None
selected_preset_paths = None
cursor_process = None

# Create main menu frame
mainmenu = ctk.CTkFrame(root, width=1280, height=720, fg_color="transparent")
mainmenu.place(relx=0.5, rely=0.5, anchor="center")

# App title
title = ctk.CTkLabel(mainmenu, text="GWBHands", font=("Segoe UI", 32, "bold"))
title.pack(pady=20)

# Cursor mode state
cursor_running = False
cursor_thread = None


def show_mainmenu():
    settings_frame.place_forget()
    how_to_use_frame.place_forget()
    gestures_frame.place_forget()

    if 'create_gestures_frame' in globals() and create_gestures_frame is not None:
        create_gestures_frame.place_forget()

    if 'change_preset_frame' in globals() and change_preset_frame is not None:
        change_preset_frame.place_forget()
        if hasattr(change_preset_frame, "edit_preset_frame") and change_preset_frame.edit_preset_frame is not None:
            change_preset_frame.edit_preset_frame.place_forget()
        if hasattr(change_preset_frame, "create_preset_frame") and change_preset_frame.create_preset_frame is not None:
            change_preset_frame.create_preset_frame.place_forget()

    mainmenu.place(relx=0.5, rely=0.5, anchor="center")

def show_settings():
    mainmenu.place_forget()
    settings_frame.place(relx=0.5, rely=0.5, anchor="center")
    
def show_changepreset():
    mainmenu.place_forget()
    settings_frame.place_forget()
    change_preset_frame.refresh_preset_list()  # Refresh preset list
    change_preset_frame.place(relx=0.5, rely=0.5, anchor="center")

def show_gestures():
    global gestures_frame

    if not selected_preset_paths or "mapping_path" not in selected_preset_paths:
        msgbox.showwarning("No Preset Selected", "Please select a preset before accessing Gestures.")
        return

    mainmenu.place_forget()

    # Destroy old gestures_frame if any
    if 'gestures_frame' in globals() and gestures_frame is not None:
        gestures_frame.destroy()
        gestures_frame = None

    # Create a fresh Gestures frame with current preset paths
    gestures_frame = Gestures(
        root,
        back_to_main_callback=show_mainmenu,
        selected_preset=selected_preset_paths,
        update_gesture_callback=update_current_preset,
        create_gesture_callback=show_create_gestures
    )
    gestures_frame.place(relx=0.5, rely=0.5, anchor="center")

def show_howtouse():
    mainmenu.place_forget()
    how_to_use_frame.place(relx=0.5, rely=0.5, anchor="center")

def show_create_gestures():
    mainmenu.place_forget()
    gestures_frame.place_forget()
    global create_gestures_frame

    # Destroy old gesture creation frame
    if 'create_gestures_frame' in globals() and create_gestures_frame is not None:
        create_gestures_frame.stop_webcam()
        create_gestures_frame.destroy()
        create_gestures_frame = None

    # Define a local callback to handle "back" AND refresh gestures list
    def on_back_from_create():
        create_gestures_frame.stop_webcam()
        create_gestures_frame.place_forget()
        show_gestures()
        if gestures_frame:  # Refresh gestures if it's loaded
            gestures_frame.refresh_gesture_list()

    # Create new gesture creation frame with selected preset
    create_gestures_frame = CreateGestures(
        root,
        back_to_gestures_callback=on_back_from_create,  # Call our callback
        selected_preset=selected_preset_paths,
        width=1280,
        height=720,
        fg_color="transparent"
    )
    create_gestures_frame.place(relx=0.5, rely=0.5, anchor="center")
    create_gestures_frame.start_webcam()

def show_createpreset():
    global create_preset_frame
    mainmenu.place_forget()

    if 'create_preset_frame' in globals() and create_preset_frame is not None:
        create_preset_frame.destroy()

    create_preset_frame = CreatePreset(
        root,
        gesture_csv_path="gestures.csv",  
        save_dir="presets",               # Preset directory
        back_callback=show_mainmenu,
        width=1280,
        height=720,
        fg_color="transparent"
    )
    create_preset_frame.place(relx=0.5, rely=0.5, anchor="center")

def update_current_preset(preset_name, preset_paths):
    global selected_preset, selected_preset_paths
    selected_preset = preset_name
    selected_preset_paths = preset_paths
    current_preset.set(f"Preset Used: {preset_name}")
    print("✅ Loaded preset paths:", preset_paths)

# In the section that initializes the change_preset_frame:
change_preset_frame = ChangePreset(
    root,
    update_preset_callback=update_current_preset,
    back_to_main_callback=show_mainmenu,
    width=1600,
    height=900,
    fg_color="transparent"
)


def toggle_cursor_default():
    global cursor_process

    if cursor_process is not None and cursor_process.poll() is None:
        cursor_process.terminate()
        cursor_process = None
        msgbox.showinfo("Cursor Mode", "Cursor mode stopped.")
        return

    python_executable = sys.executable
    start_script_path = os.path.join(os.getcwd(), "gui", "start.py")
    

    default_preset_paths = {
        "mapping_path": "gui/presets/Default/mapping.json",
        "keypoint_csv_path": "gui/presets/Default/keypoint.csv",
        "label_csv_path": "gui/presets/Default/keypoint_classifier_label.csv",
        "point_history_csv_path": "gui/presets/Default/point_history.csv"
    }

    for key, path in default_preset_paths.items():
        if not os.path.exists(path):
            msgbox.showerror("Missing File", f"{key} not found at:\n{path}")
            return

    if not os.path.exists(start_script_path):
        msgbox.showerror("File Not Found", f"start.py not found at:\n{start_script_path}")
        return

    cursor_process = subprocess.Popen([
        python_executable,
        start_script_path,
        "--mapping", default_preset_paths["mapping_path"],
        "--keypoints", default_preset_paths["keypoint_csv_path"],
        "--labels", default_preset_paths["label_csv_path"],
        "--point_history", default_preset_paths["point_history_csv_path"]
    ])

    msgbox.showinfo("Cursor Mode", "Cursor mode started.")

# Function for start button
def start_gesture_app():
    if not selected_preset:
        msgbox.showwarning("No Preset Selected", "Please select a preset before starting.")
        return

    python_executable = sys.executable

    # Since start.py is in the same folder as this file
    start_script_path = os.path.join(os.getcwd(), "gui", "start.py")


    # Debug output
    print("Launching:", start_script_path)
    print("Exists?", os.path.exists(start_script_path))

    if not os.path.exists(start_script_path):
        msgbox.showerror("File Not Found", f"start.py not found at:\n{start_script_path}")
        return
    root.withdraw()  # Add this line to hide the GUI
    root.after(1000, check_unhide_flag)
    preset_info = selected_preset_paths
    subprocess.Popen([
        python_executable,
        start_script_path,
        "--mapping", selected_preset_paths["mapping_path"],
        "--keypoints", selected_preset_paths["keypoint_csv_path"],
        "--labels", selected_preset_paths["label_csv_path"],
        "--point_history", selected_preset_paths["point_history_csv_path"]
    ])

def check_unhide_flag():
    flag_path = os.path.join(os.getcwd(), "gui", "unhide_gui.flag")
    if os.path.exists(flag_path):
        os.remove(flag_path)
        print("Unhiding main GUI")
        root.deiconify()  # Show window again
        return  # Stop checking after unhide

    # Schedule to check again in 1 second
    root.after(1000, check_unhide_flag)

def retrain_model_from_notebook():
    import os
    import nbformat
    from nbconvert.preprocessors import ExecutePreprocessor
    import tkinter.messagebox as msgbox

    # Ensure a preset is selected
    if not selected_preset:
        msgbox.showwarning("No Preset Selected", "Please select a preset before retraining.")
        return

    # Define paths
    script_dir = os.path.dirname(os.path.abspath(__file__))
    notebook_path = os.path.join(script_dir, "keypoint_classification_EN.ipynb")

    if not os.path.exists(notebook_path):
        msgbox.showerror("Notebook Not Found", f"Cannot find: {notebook_path}")
        return

    # Get preset file paths
    try:
        label_file = selected_preset_paths["label_csv_path"]
        dataset_file = selected_preset_paths["keypoint_csv_path"]
    except KeyError:
        msgbox.showerror("Preset Error", "Selected preset is missing key paths.")
        return

    # ✅ Show loading indicator
    loading_label.configure(text="🔄 Training model... Please wait.")
    mainmenu.update()

    try:
        with open(notebook_path) as f:
            nb = nbformat.read(f, as_version=4)
            nb.cells.insert(0, nbformat.v4.new_code_cell(f"label_file = r'''{label_file}'''"))
            nb.cells.insert(1, nbformat.v4.new_code_cell("print('label_file =', label_file)"))
            nb.cells.insert(2, nbformat.v4.new_code_cell(f"dataset = r'''{dataset_file}'''"))
            nb.cells.insert(3, nbformat.v4.new_code_cell("print('dataset =', dataset)"))

        ep = ExecutePreprocessor(timeout=600, kernel_name='python3')

        # Optional: pass environment variables
        os.environ["LABEL_CSV"] = label_file
        os.environ["KEYPOINT_CSV"] = dataset_file

        ep.preprocess(nb, {'metadata': {'path': script_dir}})
        msgbox.showinfo("Success", "Model trained successfully.")

    except Exception as e:
        msgbox.showerror("Error", f"An error occurred:\n{str(e)}")

    finally:
        # ✅ Hide loading indicator
        loading_label.configure(text="")
        mainmenu.update()

# Buttons
button_font = ("Segoe UI", 16)
button_width = 300
button_height = 40

btn_start = ctk.CTkButton(mainmenu, text="Start", font=button_font, width=button_width, height=button_height, command=start_gesture_app)
btn_start.pack(pady=10)

btn_preset = ctk.CTkButton(mainmenu, textvariable=current_preset, font=button_font, width=button_width, state="disabled")
btn_preset.pack(pady=10)

btn_changepreset = ctk.CTkButton(mainmenu, text="Change Preset", font=button_font, width=button_width, height=button_height, command=show_changepreset)
btn_changepreset.pack(pady=10)

btn_gestures = ctk.CTkButton(mainmenu, text="Gestures", font=button_font, width=button_width, height=button_height, command=show_gestures)
btn_gestures.pack(pady=10)

btn_retrain = ctk.CTkButton(mainmenu,text="Retrain Model",font=button_font,width=button_width,height=button_height,command=retrain_model_from_notebook)
btn_retrain.pack(pady=10)

loading_label = ctk.CTkLabel(mainmenu, text="")
loading_label.pack(pady=5)

btn_tutorial = ctk.CTkButton(mainmenu, text="How To Use", font=button_font, width=button_width, height=button_height, command=show_howtouse)
btn_tutorial.pack(pady=10)

btn_settings = ctk.CTkButton(mainmenu, text="Settings", font=button_font, width=button_width, height=button_height, command=show_settings)
btn_settings.pack(pady=10)

btn_cursor_mode = ctk.CTkButton(mainmenu, text="Toggle Cursor Mode", font=button_font,width=button_width, height=button_height, command=toggle_cursor_default)
btn_cursor_mode.pack(pady=10)

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

create_preset_frame = CreatePreset(root, gesture_csv_path="gestures.csv", save_dir="presets", back_callback=show_mainmenu, update_presets_callback=change_preset_frame.refresh_preset_list, width=1280, height=720, fg_color="transparent")
create_preset_frame.place_forget()


# Create Gestures frame but hidden until accessed
gestures_frame = Gestures(
    root,
    back_to_main_callback=show_mainmenu,
    update_gesture_callback=update_current_preset,
    create_gesture_callback=show_create_gestures
)
gestures_frame.place_forget()

# Start the GUI loop
root.mainloop()