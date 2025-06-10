import os
import cv2
import numpy as np
import mediapipe as mp
from tensorflow.keras.models import load_model  # type: ignore
import pyautogui

# Dynamically build the path to the model file
base_dir = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(base_dir, "models", "gesture_recognition_model.h5")

# Load model
model = load_model(model_path)
print("Model loaded successfully!")

# Define your gesture classes in the same order as training
GESTURE_CLASSES = ["thumbs_up", "thumbs_down", "peace", "fist", "open_hand"]  # <-- update as needed

# Map gestures to keyboard keys
gesture_to_key = {
    "thumbs_up": "w",
    "thumbs_down": "s",
    "peace": "a",
    "fist": "d",
    "open_hand": "space"
}
