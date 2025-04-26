import customtkinter as ctk
import cv2
from pygrabber.dshow_graph import FilterGraph
from test_webcam import TestWebcam

class SettingsPage(ctk.CTkFrame):
    def __init__(self, master, back_to_main_callback, **kwargs):
        super().__init__(master, **kwargs)
        self.back_to_main_callback = back_to_main_callback

        # Detect available webcams
        self.detected_webcams = self.detect_webcam()
        self.gesture_detection_value = ctk.IntVar(value=0)
        self.gesture_overlay_value = ctk.IntVar(value=0)

        self.create_widgets()

    
    def detect_webcam(self, maxdevices=20):
        graph = FilterGraph()
        device_names = graph.get_input_devices()

        cameras = []
        for i in range(min(maxdevices, len(device_names))):
            cap = cv2.VideoCapture(i, cv2.CAP_DSHOW)
            if cap is not None and cap.isOpened():
                cameras.append(device_names[i])
                cap.release()
    
        return cameras if cameras else ["No webcam found"]
    
    def test_webcam(self):
        TestWebcam(self)
    

    def create_widgets(self):
        font_ui = "Segoe UI"
           
        # Title
        title = ctk.CTkLabel(self, text="Settings", font=(font_ui, 32, "bold"))
        title.pack(pady=20)

        # Webcam settings
        webcam_label = ctk.CTkLabel(self, text="Webcam:", font=(font_ui, 16, "bold"))
        webcam_label.pack(pady=10)

        self.webcam_list = ctk.CTkOptionMenu(self, values=self.detected_webcams)
        self.webcam_list.set(self.detected_webcams[0])
        self.webcam_list.pack(pady=10)
        
        test_webcam_button = ctk.CTkButton(self, text="Test Webcam", command=self.test_webcam, font=(font_ui, 16, "bold"))
        test_webcam_button.pack(pady=10)
        

        # Gesture Detection 
        gesture_detection_label = ctk.CTkLabel(self, text="Gesture Detection:", font=(font_ui, 16, "bold"))
        gesture_detection_label.pack(pady=10)

        button_font = (font_ui, 16)
        detection_on = ctk.CTkRadioButton(self, text="On", variable=self.gesture_detection_value, value=1, font=button_font)
        detection_off = ctk.CTkRadioButton(self, text="Off", variable=self.gesture_detection_value, value=0, font=button_font)
        detection_on.pack(pady=10)
        detection_off.pack(pady=10)

        # Gesture Overlay 
        gesture_overlay_label = ctk.CTkLabel(self, text="Gesture Overlay:", font=(font_ui, 16, "bold"))
        gesture_overlay_label.pack(pady=10)

        overlay_on = ctk.CTkRadioButton(self, text="On", variable=self.gesture_overlay_value, value=1, font=button_font)
        overlay_off = ctk.CTkRadioButton(self, text="Off", variable=self.gesture_overlay_value, value=0, font=button_font)
        overlay_on.pack(pady=10)
        overlay_off.pack(pady=10)

        # Save and Cancel buttons
        save_button = ctk.CTkButton(self, text="Save", command=self.save_and_return, font=(font_ui, 16, "bold"))
        cancel_button = ctk.CTkButton(self, text="Cancel", command=self.cancel_and_return, font=(font_ui, 16, "bold"))
        save_button.pack(pady=10)
        cancel_button.pack(pady=10)

    def save_and_return(self):
        # To add logic to save settings later
        self.back_to_main_callback()

    def cancel_and_return(self):
        self.back_to_main_callback()