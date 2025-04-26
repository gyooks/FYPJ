import cv2
import customtkinter as ctk
from PIL import Image, ImageTk

class TestWebcam(ctk.CTkToplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Webcam Test")
        self.geometry("640x480")
        
        self.video_label = ctk.CTkLabel(self, text = "")
        self.video_label.pack(pady=20)
        
        self.cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        if not self.cap.isOpened():
            print("Error: Could not open webcam.")
            self.destroy()
            return
        
        self.update_frames()
        
    def update_frames(self):
        ret, frame = self.cap.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(frame)
            imgtk = ImageTk.PhotoImage(img)
            
            self.video_label.configure(image=imgtk)
            self.video_label.image = imgtk
            
        self.after(10, self.update_frames)
        
    def on_close(self):
        self.cap.release()
        self.destroy()