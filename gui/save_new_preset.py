import csv
import json
import os

# Paths
label_csv_path = 'model/keypoint_classifier/keypoint_classifier_label.csv'
preset_json_path = 'presets/new_preset.json'

# Load gesture labels from CSV
with open(label_csv_path, encoding='utf-8-sig') as f:
    gesture_labels = [row[0] for row in csv.reader(f)]

print("Available Gestures:")
for idx, label in enumerate(gesture_labels):
    print(f"{idx}: {label}")

# User input for mappings
gesture_to_key = {}
while True:
    idx = input("\nEnter gesture index (or 'q' to quit): ")
    if idx.lower() == 'q':
        break

    try:
        idx = int(idx)
        gesture = gesture_labels[idx]
    except (ValueError, IndexError):
        print("Invalid index. Try again.")
        continue

    key = input(f"Map gesture '{gesture}' to which key? (e.g., w, enter): ").strip()
    gesture_to_key[gesture] = key

# Save to JSON
os.makedirs(os.path.dirname(preset_json_path), exist_ok=True)
with open(preset_json_path, 'w') as f:
    json.dump(gesture_to_key, f, indent=4)

print(f"\nPreset saved to {preset_json_path}")
