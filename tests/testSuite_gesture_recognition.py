import pytest
import numpy as np
import json
import csv
import sys
import time
from gui.start import KeyPointClassifier

from unittest.mock import patch
from gui.start import calc_landmark_list, pre_process_landmark, KeyPointClassifier, main

def test_calc_landmark_list():
    image = np.zeros((540, 960, 3), dtype=np.uint8)
    class MockLandmark:
        def __init__(self, x, y):
            self.x = x
            self.y = y
    class MockLandmarks:
        landmark = [MockLandmark(0.5, 0.5), MockLandmark(0.3, 0.3)]
    
    landmarks = MockLandmarks()
    result = calc_landmark_list(image, landmarks)
    
    assert len(result) == 2
    assert result[0] == [480, 270]
    assert result[1] == [288, 162]

def test_pre_process_landmark():
    landmark_list = [[100, 200], [150, 250]]
    result = pre_process_landmark(landmark_list)
    
    expected = [0.0, 0.0, 1.0, 1.0]
    assert len(result) == 4
    assert all(abs(result[i] - expected[i]) < 1e-6 for i in range(4))

def test_gesture_recognition_latency():
    classifier = KeyPointClassifier()
    # Mock pre-processed landmarks (42 values for 21 landmarks)
    landmarks = [0.1] * 42
    
    start_time = time.time()
    classifier(landmarks)
    end_time = time.time()
    
    latency = end_time - start_time
    assert latency < 0.1, f"Latency {latency}s exceeds 100ms"