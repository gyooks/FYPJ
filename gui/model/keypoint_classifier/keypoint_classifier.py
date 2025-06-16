#!/usr/bin/env python
# -*- coding: utf-8 -*-
import numpy as np
import tensorflow as tf
import os

class KeyPointClassifier(object):
    def __init__(
        self,
        model_path=None,
        num_threads=1,
    ):
        # Dynamically resolve the correct path relative to this file
        if model_path is None:
            script_dir = os.path.dirname(os.path.abspath(__file__))
            model_path = os.path.join(script_dir, 'keypoint_classifier.tflite')

        if not os.path.exists(model_path):
            raise ValueError(f"Could not open model file. Path does not exist: {model_path}")

        self.interpreter = tf.lite.Interpreter(model_path=model_path,
                                               num_threads=num_threads)
        self.interpreter.allocate_tensors()
        self.input_details = self.interpreter.get_input_details()
        self.output_details = self.interpreter.get_output_details()

    def __call__(self, landmark_list):
        input_details_tensor_index = self.input_details[0]['index']
        self.interpreter.set_tensor(
            input_details_tensor_index,
            np.array([landmark_list], dtype=np.float32))
        self.interpreter.invoke()

        output_details_tensor_index = self.output_details[0]['index']
        result = self.interpreter.get_tensor(output_details_tensor_index)
        result_index = np.argmax(np.squeeze(result))

        return result_index
