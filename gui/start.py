import os
import cv2
import numpy as np
import mediapipe as mp
from tensorflow.keras.models import load_model  # type: ignore
import pyautogui
from collections import deque
import time

# === Load model ===
base_dir = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(base_dir, "models", "gesture_recognition_model.h5")
model = load_model(model_path)
print("Model loaded successfully!")

# === Gesture classes & key mapping ===
GESTURE_CLASSES = ["thumbs_up", "thumbs_down", "peace", "fist", "open_hand"]

gesture_to_key = {
    "thumbs_up": "w",
    "thumbs_down": "s",
    "peace": "a",
    "fist": "d",
    "open_hand": "space"
}

# === MediaPipe setup ===
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=1, min_detection_confidence=0.7)
mp_draw = mp.solutions.drawing_utils

# === Frame buffer (sequence of 30 frames) ===
sequence = deque(maxlen=30)

# === Gesture cooldown settings ===
cooldown = 2  # seconds between accepting same gesture
last_prediction = None
last_action_time = time.time()

# === GUI toggle ===
display_window = True  # 'h' key toggles this

# === Start webcam ===
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(img_rgb)

    if results.multi_hand_landmarks:
        landmarks = results.multi_hand_landmarks[0]

        hand_data = []
        for lm in landmarks.landmark:
            hand_data.extend([lm.x, lm.y, lm.z])  # 63 features

        mp_draw.draw_landmarks(frame, landmarks, mp_hands.HAND_CONNECTIONS)

        input_data = np.expand_dims(hand_data, axis=0)  # (1, 63)

        prediction = model.predict(input_data, verbose=0)
        predicted_class = GESTURE_CLASSES[np.argmax(prediction)]

        cv2.putText(frame, f"Gesture: {predicted_class}", (10, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        current_time = time.time()
        if predicted_class != last_prediction or (current_time - last_action_time) > cooldown:
            pyautogui.press(gesture_to_key[predicted_class])
            last_action_time = current_time
            last_prediction = predicted_class

    else:
        sequence.clear()

    if display_window:
        cv2.imshow("Gesture Control", frame)

    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break
    elif key == ord("h"):  # toggle visibility
        display_window = not display_window
        if not display_window:
            cv2.destroyWindow("Gesture Control")

cap.release()
cv2.destroyAllWindows()
