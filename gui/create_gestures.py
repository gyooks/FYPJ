import customtkinter as ctk
import cv2
from PIL import Image

class CreateGestures(ctk.CTkFrame):
    def __init__(self, master, back_to_gestures_callback, **kwargs):
        super().__init__(master, **kwargs)
        self.back_to_gestures_callback = back_to_gestures_callback

        self.cap = None
        self.is_running = False

        self.WIDTH = 640
        self.HEIGHT = 480

        self.create_widgets()
        self.start_webcam()  # Start webcam automatically on frame creation

    def create_widgets(self):
        font_ui = "Segoe UI"
        button_font = (font_ui, 16)

        title = ctk.CTkLabel(self, text="Create Gesture", font=(font_ui, 32, "bold"))
        title.pack(pady=20)

        self.video_label = ctk.CTkLabel(self, width=self.WIDTH, height=self.HEIGHT, text="")
        self.video_label.pack(pady=10)

        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.pack(pady=20)

        save_btn = ctk.CTkButton(btn_frame, text="Save", font=button_font, command=self.save_gesture)
        save_btn.grid(row=0, column=0, padx=10)

        back_btn = ctk.CTkButton(btn_frame, text="Back", font=button_font, command=self.go_back)
        back_btn.grid(row=0, column=1, padx=10)

    def start_webcam(self):
        if not self.is_running:
            self.cap = cv2.VideoCapture(0)
            if not self.cap.isOpened():
                print("Error: Could not open webcam.")
                return
            self.is_running = True
            self.update_frame()

    def save_gesture(self):
        # Implement your saving logic here
        print("Save button clicked - implement gesture saving here.")

    def stop_webcam(self):
        if self.is_running:
            self.is_running = False
            if self.cap:
                self.cap.release()
                self.cap = None
            self.video_label.configure(image=None)
            self.video_label.image = None

    def update_frame(self):
        if not self.is_running:
            return

        ret, frame = self.cap.read()
        if ret:
            # Resize frame to forced size
            frame = cv2.resize(frame, (self.WIDTH, self.HEIGHT))
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(frame)

            # Convert PIL image to CTkImage with forced size to match label
            ctk_img = ctk.CTkImage(img, size=(self.WIDTH, self.HEIGHT))

            self.video_label.configure(image=ctk_img)
            self.video_label.image = ctk_img
        else:
            print("Failed to grab frame")

        self.after(15, self.update_frame)

    def go_back(self):
        self.stop_webcam()
        self.place_forget()
        self.back_to_gestures_callback()


if __name__ == "__main__":
    def dummy_back():
        print("Back pressed")

    root = ctk.CTk()
    root.geometry("900x700")
    root.title("Test CreateGestures")

    frame = CreateGestures(root, back_to_gestures_callback=dummy_back)
    frame.pack(expand=True, fill="both")

    root.mainloop()