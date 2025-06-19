import customtkinter as ctk
import cv2
from PIL import Image
import mediapipe as mp
import os


class CreateGestures(ctk.CTkFrame):
    def __init__(self, master, back_to_gestures_callback, selected_preset=None, **kwargs):
        super().__init__(master, **kwargs)
        self.back_to_gestures_callback = back_to_gestures_callback
        self.selected_preset = selected_preset or {}

        self.cap = None
        self.is_running = False
        self.WIDTH = 640
        self.HEIGHT = 480

        # Get CSV path from preset (fallback if missing)
        self.csv_path = self.selected_preset.get("label_csv_path", "keypoint_classifier_label.csv")
        self.current_gesture_name = None

        # Initialize MediaPipe Hands
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=2,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.5
        )
        self.mp_drawing = mp.solutions.drawing_utils

        self.create_widgets()
        self.start_webcam()

    def create_widgets(self):
        font_ui = "Segoe UI"
        button_font = (font_ui, 16)

        title = ctk.CTkLabel(self, text="Create Gesture", font=(font_ui, 32, "bold"))
        title.pack(pady=20)

        self.video_label = ctk.CTkLabel(self, width=self.WIDTH, height=self.HEIGHT, text="")
        self.video_label.pack(pady=10)

        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.pack(pady=20)

        start_record_btn = ctk.CTkButton(btn_frame, text="Start Recording", font=button_font, command=self.start_recording)
        start_record_btn.grid(row=0, column=0, padx=10)

        capture_btn = ctk.CTkButton(btn_frame, text="Capture", font=button_font, command=self.capture)
        capture_btn.grid(row=0, column=1, padx=10)

        save_btn = ctk.CTkButton(btn_frame, text="Stop to Save", font=button_font, command=self.save_gesture)
        save_btn.grid(row=0, column=2, padx=10)

        back_btn = ctk.CTkButton(btn_frame, text="Back", font=button_font, command=self.go_back)
        back_btn.grid(row=0, column=3, padx=10)

    def start_webcam(self):
        if not self.is_running:
            self.cap = cv2.VideoCapture(0)
            if not self.cap.isOpened():
                print("❌ Error: Could not open webcam.")
                return
            self.is_running = True
            self.update_frame()

    def start_recording(self):
        dialog = ctk.CTkInputDialog(title="Gesture Name", text="Enter gesture name:")
        gesture_name = dialog.get_input()

        if gesture_name:
            self.current_gesture_name = gesture_name.strip()
            print(f"🟢 Recording started for gesture: {self.current_gesture_name}")
        else:
            self.current_gesture_name = None
            print("⚠️ Gesture name input canceled.")

    def capture(self):
        # Optional: implement later to collect hand landmarks
        print("📸 Capture clicked - implement logic here if needed.")

    def save_gesture(self):
        if not self.current_gesture_name:
            print("❌ No gesture name provided.")
            return

        try:
            # Ensure directory exists
            os.makedirs(os.path.dirname(self.csv_path), exist_ok=True)

            # Check if file ends with newline
            needs_newline = False
            if os.path.exists(self.csv_path):
                with open(self.csv_path, 'rb') as f:
                    f.seek(-1, os.SEEK_END)
                    last_char = f.read(1)
                    if last_char != b'\n':
                        needs_newline = True

            # Append the gesture name, preceded by newline if needed
            with open(self.csv_path, mode='a', encoding='utf-8') as f:
                if needs_newline:
                    f.write('\n')
                f.write(self.current_gesture_name + '\n')

            print(f"✅ Gesture '{self.current_gesture_name}' saved to {self.csv_path}")
            self.current_gesture_name = None

        except Exception as e:
            print(f"❌ Error saving gesture: {e}")

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
            frame = cv2.flip(frame, 1)
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = self.hands.process(frame_rgb)

            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    self.mp_drawing.draw_landmarks(
                        frame,
                        hand_landmarks,
                        self.mp_hands.HAND_CONNECTIONS,
                        self.mp_drawing.DrawingSpec(color=(255, 255, 255), thickness=2, circle_radius=2),
                        self.mp_drawing.DrawingSpec(color=(255, 255, 255), thickness=2, circle_radius=2)
                    )

            frame = cv2.resize(frame, (self.WIDTH, self.HEIGHT))
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(frame_rgb)
            ctk_img = ctk.CTkImage(img, size=(self.WIDTH, self.HEIGHT))

            self.video_label.configure(image=ctk_img)
            self.video_label.image = ctk_img
        else:
            print("❌ Failed to grab frame")

        self.after(15, self.update_frame)

    def go_back(self):
        self.stop_webcam()
        self.place_forget()
        self.back_to_gestures_callback()


# Optional test run
if __name__ == "__main__":
    def dummy_back():
        print("Back pressed")

    root = ctk.CTk()
    root.geometry("900x700")
    root.title("Test CreateGestures")

    frame = CreateGestures(root, back_to_gestures_callback=dummy_back, selected_preset={"label_csv_path": "keypoint_classifier_label.csv"})
    frame.pack(expand=True, fill="both")

    root.mainloop()