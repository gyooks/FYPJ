import cv2
import mediapipe as mp
import pyautogui
import threading

class HandCursor:
    def __init__(self, draw_cursor=True):
        self.running = False
        self.draw_cursor = draw_cursor
        self.cap = None
        self.thread = None

        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7)
        self.mp_draw = mp.solutions.drawing_utils

        self.screen_width, self.screen_height = pyautogui.size()

    def start(self):
        if self.running:
            return
        self.running = True
        self.thread = threading.Thread(target=self.track_hand)
        self.thread.start()

    def stop(self):
        self.running = False
        if self.cap:
            self.cap.release()

    def track_hand(self):
        self.cap = cv2.VideoCapture(0)

        while self.running:
            ret, frame = self.cap.read()
            if not ret:
                continue

            frame = cv2.flip(frame, 1)
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = self.hands.process(rgb)

            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    # Index finger tip
                    x = hand_landmarks.landmark[self.mp_hands.HandLandmark.INDEX_FINGER_TIP].x
                    y = hand_landmarks.landmark[self.mp_hands.HandLandmark.INDEX_FINGER_TIP].y

                    # Convert to screen coordinates
                    screen_x = int(self.screen_width * x)
                    screen_y = int(self.screen_height * y)

                    # Move mouse
                    pyautogui.moveTo(screen_x, screen_y)

            # Optional: show webcam feed
            if self.draw_cursor:
                cv2.imshow("Hand Cursor", frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

        self.cap.release()
        cv2.destroyAllWindows()
