import os
import cv2
import numpy as np
import mediapipe as mp
from tensorflow.keras.models import load_model  # type: ignore
import pyautogui
from collections import deque

# === Load model ===
base_dir = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(base_dir, "models", "gesture_recognition_model.h5")
model = load_model(model_path)
print("Model loaded successfully!")

# === Gesture classes & key mapping ===
GESTURE_CLASSES = ["thumbs_up", "thumbs_down", "peace", "fist", "open_hand"]  # update as needed

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

# === Frame buffer (deque for sequence of 30 frames) ===
sequence = deque(maxlen=30)

# === Start webcam ===
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Flip frame (mirror view)
    frame = cv2.flip(frame, 1)
    img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(img_rgb)

    if results.multi_hand_landmarks:
        landmarks = results.multi_hand_landmarks[0]
        # Flatten 21 hand landmarks (x, y, z) into a 63-element array
        hand_data = []
        for lm in landmarks.landmark:
            hand_data.extend([lm.x, lm.y, lm.z])

        sequence.append(hand_data)

        # Draw landmarks on frame
        mp_draw.draw_landmarks(frame, landmarks, mp_hands.HAND_CONNECTIONS)

        if len(sequence) == 30:
            input_seq = np.expand_dims(sequence, axis=0)  # Shape: (1, 30, 63)
            prediction = model.predict(input_seq, verbose=0)
            predicted_class = GESTURE_CLASSES[np.argmax(prediction)]

            # Display prediction
            cv2.putText(frame, f"Gesture: {predicted_class}", (10, 50),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

            # Send key press
            pyautogui.press(gesture_to_key[predicted_class])

    else:
        # Clear sequence if no hand detected
        sequence.clear()

    cv2.imshow("Gesture Control", frame)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
