# settings.py
import customtkinter as ctk
import cv2

class SettingsPage(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        def detect_webcam(maxdevices=3):
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

        # Title
        title = ctk.CTkLabel(self, text="Settings", font=("Segoe UI", 32, "bold"))
        title.pack(pady=20)

        # Webcam
        webcam = ctk.CTkLabel(self, text="Webcam:", font=("Segoe UI", 16, "bold"))
        webcam.pack(pady=10)

        webcam_list = ctk.CTkOptionMenu(self, values=detected_webcams)
        webcam_list.set(detected_webcams[0])
        webcam_list.pack(pady=10)

        # Gesture Detection
        gesture_detection = ctk.CTkLabel(self, text="Gesture Detection:", font=("Segoe UI", 16, "bold"))
        gesture_detection.pack(pady=10)

        button_font = ("Segoe UI", 16)
        detection_on = ctk.CTkRadioButton(self, text="On", variable=gesture_detection_value, value=1, font=button_font)
        detection_off = ctk.CTkRadioButton(self, text="Off", variable=gesture_detection_value, value=0, font=button_font)
        detection_on.pack(pady=10)
        detection_off.pack(pady=10)

        # Gesture Overlay
        gesture_overlay = ctk.CTkLabel(self, text="Gesture Overlay:", font=("Segoe UI", 16, "bold"))
        gesture_overlay.pack(pady=10)

        overlay_on = ctk.CTkRadioButton(self, text="On", variable=gesture_overlay_value, value=1, font=button_font)
        overlay_off = ctk.CTkRadioButton(self, text="Off", variable=gesture_overlay_value, value=0, font=button_font)
        overlay_on.pack(pady=10)
        overlay_off.pack(pady=10)

        # Save and Cancel buttons
        save_settings = ctk.CTkButton(self, text="Save", command=master.quit, font=("Segoe UI", 16, "bold"))
        cancel_settings = ctk.CTkButton(self, text="Cancel", command=master.quit, font=("Segoe UI", 16, "bold"))
        save_settings.pack(pady=10)
        cancel_settings.pack(pady=10)