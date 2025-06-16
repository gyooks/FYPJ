import sys
#testing
PRESETS = [
    {
        "name": "Racing Game",
        "gesture_classes": [
            "steer_left", "steer_right", "pause", "boost", "accelerate", "brake"
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
    {
        "name": "Empty",
        "gesture_classes": [],
        "gesture_to_key": {}
    },
    {
        "name": "Empty",
        "gesture_classes": [],
        "gesture_to_key": {}
    }
]