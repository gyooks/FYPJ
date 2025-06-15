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

PRESETS = {
    "Preset 1": {
        "name": "Racing Game",
        "gesture_classes": [
            "steer_left",
            "steer_right",
            "pause",
            "boost",
            "accelerate",
            "brake"
        ],
        "gesture_to_key": {
            "steer_left": "left",
            "steer_right": "right",
            "accelerate": "w",
            "brake": "s",
            "boost": "shift",
            "pause": "esc"
        }
    },
    "Preset 2": {
        "name": "Empty",
        "gesture_classes": [],
        "gesture_to_key": {}
    },
    "Preset 3": {
        "name": "Empty",
        "gesture_classes": [],
        "gesture_to_key": {}
    }
}

# === MediaPipe setup (2 hands) ===
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=2, min_detection_confidence=0.7)
mp_draw = mp.solutions.drawing_utils

# === Buffers for left and right hands ===
sequence_left = deque(maxlen=29)
sequence_right = deque(maxlen=29)

# === Gesture cooldown ===
cooldown = 2
last_prediction_left = None
last_prediction_right = None
last_action_time_left = time.time()
last_action_time_right = time.time()

# === GUI toggle ===
display_window = True

# === Start webcam ===
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(img_rgb)

    if results.multi_hand_landmarks and results.multi_handedness:
        for hand_landmarks, handedness in zip(results.multi_hand_landmarks, results.multi_handedness):
            label = handedness.classification[0].label  # 'Left' or 'Right'
            wrist = hand_landmarks.landmark[0]
            hand_data = [wrist.x, wrist.y]

            if label == "Left":
                sequence_left.append(hand_data)
            elif label == "Right":
                sequence_right.append(hand_data)

            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

    # === Process Left Hand ===
    if len(sequence_left) == 29:
        input_left = np.expand_dims(sequence_left, axis=0)
        prediction_left = model.predict(input_left, verbose=0)
        predicted_index = np.argmax(prediction_left)
        confidence = np.max(prediction_left)
        predicted_class = GESTURE_CLASSES[predicted_index]

        print(f"[Left Hand] Predicted: {predicted_class} (confidence: {confidence:.2f})")

        cv2.putText(frame, f"Left: {predicted_class}", (10, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

        current_time = time.time()
        if predicted_class != last_prediction_left or (current_time - last_action_time_left) > cooldown:
            key = gesture_to_key.get(predicted_class)
            if key:
                pyautogui.press(key)
                print(f"[Left Hand] Sent key: {key}")
            last_action_time_left = current_time
            last_prediction_left = predicted_class

    # === Process Right Hand ===
    if len(sequence_right) == 29:
        input_right = np.expand_dims(sequence_right, axis=0)
        prediction_right = model.predict(input_right, verbose=0)
        predicted_index = np.argmax(prediction_right)
        confidence = np.max(prediction_right)
        predicted_class = GESTURE_CLASSES[predicted_index]

        print(f"[Right Hand] Predicted: {predicted_class} (confidence: {confidence:.2f})")

        cv2.putText(frame, f"Right: {predicted_class}", (10, 100),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)

        current_time = time.time()
        if predicted_class != last_prediction_right or (current_time - last_action_time_right) > cooldown:
            key = gesture_to_key.get(predicted_class)
            if key:
                pyautogui.press(key)
                print(f"[Right Hand] Sent key: {key}")
            last_action_time_right = current_time
            last_prediction_right = predicted_class

    # === Display GUI ===
    if display_window:
        cv2.imshow("Gesture Control - Dual Hand", frame)

    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break
    elif key == ord("h"):
        display_window = not display_window
        if not display_window:
            cv2.destroyWindow("Gesture Control - Dual Hand")

cap.release()
cv2.destroyAllWindows()