import customtkinter as ctk
import cv2

root = ctk.CTk()
ctk.set_appearance_mode("dark") 
ctk.set_default_color_theme("blue")

# Set the title and size of the window
root.title("Settings")
root.geometry("1024x968")

def detect_webcam(maxdevices=3):
    #detects all available webcams
    cameras = []
    for i in range(maxdevices):
        cap = cv2.VideoCapture(i, cv2.CAP_DSHOW)
        if cap is not None and cap.isOpened():
            cameras.append(f"Webcam {i}")
            cap.release()
    return cameras if cameras else ["No webcam found"]

detected_webcams = detect_webcam()
gesture_detection_value = ctk.IntVar(value=0)
gesture_overlay_value = ctk.IntVar(value=0)

# Create a frame to hold the widgets
center = ctk.CTkFrame(root, width=1600, height=900, fg_color="transparent")
center.place(relx=0.5, rely=0.5, anchor="center")

#App title
title = ctk.CTkLabel(root, text="Settings", font=("Segoe UI", 32, "bold"))
title.pack(pady=20)
title.place(relx=0.5, rely=0.1, anchor="center")

#Setting options
webcam = ctk.CTkLabel(center, text="Webcam:", font=("Segoe UI", 16, "bold"))
webcam.pack(pady=10)

#webcam list
webcam_list = ctk.CTkOptionMenu(center, values=detected_webcams)
webcam_list.set(detected_webcams[0])
webcam_list.pack(pady=10)

#Gesture detection toggle
gesture_detection = ctk.CTkLabel(center, text="Gesture Detection:", font=("Segoe UI", 16, "bold"))
gesture_detection.pack(pady=10)

button_font = ("Segoe UI", 16)
detection_on = ctk.CTkRadioButton(center, text="On", variable= gesture_detection_value, value=1, font=button_font)
detection_off = ctk.CTkRadioButton(center, text="Off", variable= gesture_detection_value, value=0, font=button_font)
detection_on.pack(pady=10) 
detection_off.pack(pady=10)

gesture_overlay = ctk.CTkLabel(center, text="Gesture Overlay:", font=("Segoe UI", 16, "bold"))
gesture_overlay.pack(pady=10)

overlay_on = ctk.CTkRadioButton(center, text="On", variable= gesture_overlay_value, value=1, font=button_font)
overlay_off = ctk.CTkRadioButton(center, text="Off", variable= gesture_overlay_value, value=0, font=button_font)
overlay_on.pack(pady=10)
overlay_off.pack(pady=10)

save_settings = ctk.CTkButton(center, text="Save", command=root.quit, font=("Segoe UI", 16, "bold"))
cancel_settings = ctk.CTkButton(center, text="Cancel", command=root.quit, font=("Segoe UI", 16, "bold"))
save_settings.pack(pady=10)
cancel_settings.pack(pady=10)
root.mainloop()
