import cv2
import numpy as np
import pyautogui
import mediapipe as mp
import json
import sys
import os
from model import KeyPointClassifier

# ========== Paths ==========
# Dynamically add the model folder to sys.path
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_DIR = os.path.join(SCRIPT_DIR, '..', 'model')
sys.path.append(MODEL_DIR)

PRESET_NAME = "Default"
BASE_PATH = os.path.join("gui", "presets", PRESET_NAME)
MODEL_PATH = os.path.join("gui","model","keypoint_classifier","keypoint_classifier.tflite")
LABEL_PATH = os.path.join(BASE_PATH, "keypoint_classifier_label.csv")
MAPPING_PATH = os.path.join(BASE_PATH, "mapping.json")

# ========== Load labels ==========
with open(LABEL_PATH, encoding='utf-8') as f:
    gesture_labels = [line.strip() for line in f.readlines()]

# ========== Load mappings ==========
with open(MAPPING_PATH, encoding='utf-8') as f:
    gesture_mapping = json.load(f)

# ========== Init classifier ==========
keypoint_classifier = KeyPointClassifier(model_path=MODEL_PATH)


# ========== Init MediaPipe Hands ==========
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    max_num_hands=1,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)
mp_drawing = mp.solutions.drawing_utils

# ========== Init webcam and screen ==========
cap = cv2.VideoCapture(0)
screen_width, screen_height = pyautogui.size()
prev_gesture = None

print("🟢 Cursor + Gesture (Default Preset) Mode Started")

try:
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.flip(frame, 1)
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(image)
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)

                # Get 21 keypoints
                landmark_list = []
                for lm in hand_landmarks.landmark:
                    landmark_list.append([lm.x, lm.y])

                # Normalize landmarks
                base_x, base_y = landmark_list[0]
                relative_landmarks = []
                for x, y in landmark_list:
                    relative_landmarks.append(x - base_x)
                    relative_landmarks.append(y - base_y)

                # Gesture classification
                gesture_id = keypoint_classifier(relative_landmarks)
                gesture_name = gesture_labels[gesture_id]

                # Debugging
                print(f"Detected gesture: {gesture_name}")

                # Move cursor with index finger
                index_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
                cursor_x = int(index_tip.x * screen_width)
                cursor_y = int(index_tip.y * screen_height)
                pyautogui.moveTo(cursor_x, cursor_y)

                # Action mapping
                action = gesture_mapping.get(gesture_name)
                if action:
                    if action == "left_click":
                        if prev_gesture != gesture_name:
                            pyautogui.click()
                        prev_gesture = gesture_name
                else:
                    prev_gesture = None

        cv2.imshow('Cursor Mode (Default)', image)
        if cv2.waitKey(1) & 0xFF == 27:  # ESC to exit
            break

except Exception as e:
    print(f"❌ Error: {e}")

finally:
    cap.release()
    cv2.destroyAllWindows()
    print("🎥 Webcam released.")
