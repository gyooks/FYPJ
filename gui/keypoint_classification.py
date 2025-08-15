# keypoint_classification.py
import csv
import os
import sys
import numpy as np
import tensorflow as tf
from sklearn.model_selection import train_test_split
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix, classification_report

RANDOM_SEED = 42



def resource_path(relative_path):
    """Get absolute path to resource, works for dev and PyInstaller EXE"""
    try:
        base_path = sys._MEIPASS  # PyInstaller temp dir
    except Exception:
        base_path = os.path.dirname(os.path.abspath(__file__))  # script dir
    return os.path.join(base_path, relative_path)

def get_model_paths():
    """
    Returns correct paths for model saving/loading for both script and PyInstaller EXE.
    """
    if getattr(sys, 'frozen', False):
        # Running as PyInstaller exe
        # Get folder where EXE is located
        exe_dir = os.path.dirname(sys.executable)

        # If 'gui' folder exists next to exe, use it
        base_path = os.path.join(exe_dir, "gui")
        if not os.path.exists(base_path):
            # If running exe directly inside gui, go up one level
            base_path = exe_dir
    else:
        # Running as a normal script
        base_path = os.path.dirname(os.path.abspath(__file__))

    model_dir = os.path.join(base_path, "model", "keypoint_classifier")
    os.makedirs(model_dir, exist_ok=True)

    model_save_path = os.path.join(model_dir, "keypoint_classifier.keras")
    tflite_save_path = os.path.join(model_dir, "keypoint_classifier.tflite")
    return model_dir, model_save_path, tflite_save_path

def run_training(label_file, dataset_file):
    model_dir, model_save_path, tflite_save_path = get_model_paths()

    # Debug print
    print(f"Using label file: {label_file}")
    print(f"Using dataset file: {dataset_file}")
    print(f"Keras model will be saved to: {model_save_path}")
    print(f"TFLite model will be saved to: {tflite_save_path}")

    # --- Load label file ---
    with open(label_file, 'r', encoding='utf-8') as f:
        label_list = [row for row in csv.reader(f) if row]
    NUM_CLASSES = len(label_list)
    print("Detected NUM_CLASSES:", NUM_CLASSES)

    # --- Load dataset ---
    X_dataset = np.loadtxt(dataset_file, delimiter=',', dtype='float32',
                           usecols=list(range(1, (21 * 2) + 1)))
    y_dataset = np.loadtxt(dataset_file, delimiter=',', dtype='int32', usecols=(0))

    # --- Train/test split ---
    X_train, X_test, y_train, y_test = train_test_split(
        X_dataset, y_dataset, train_size=0.75, random_state=RANDOM_SEED
    )

    # --- Build model ---
    model = tf.keras.models.Sequential([
        tf.keras.layers.Input((21 * 2, )),
        tf.keras.layers.Dropout(0.2),
        tf.keras.layers.Dense(20, activation='relu'),
        tf.keras.layers.Dropout(0.4),
        tf.keras.layers.Dense(10, activation='relu'),
        tf.keras.layers.Dense(NUM_CLASSES, activation='softmax')
    ])
    model.summary()

    # --- Callbacks ---
    cp_callback = tf.keras.callbacks.ModelCheckpoint(model_save_path, verbose=1, save_weights_only=False)
    es_callback = tf.keras.callbacks.EarlyStopping(patience=20, verbose=1)

    # --- Compile ---
    model.compile(
        optimizer='adam',
        loss='sparse_categorical_crossentropy',
        metrics=['accuracy']
    )

    # --- Train ---
    model.fit(
        X_train, y_train,
        epochs=1000,
        batch_size=128,
        validation_data=(X_test, y_test),
        callbacks=[cp_callback, es_callback]
    )

    # --- Evaluate ---
    val_loss, val_acc = model.evaluate(X_test, y_test, batch_size=128)
    print(f"Validation Accuracy: {val_acc:.4f}")

    # --- Confusion Matrix ---
    def print_confusion_matrix(y_true, y_pred, report=True):
        labels = sorted(list(set(y_true)))
        cmx_data = confusion_matrix(y_true, y_pred, labels=labels)
        df_cmx = pd.DataFrame(cmx_data, index=labels, columns=labels)

        fig, ax = plt.subplots(figsize=(7, 6))
        sns.heatmap(df_cmx, annot=True, fmt='g', square=False)
        ax.set_ylim(len(set(y_true)), 0)
        plt.savefig(os.path.join(model_dir, "confusion_matrix.png"))
        plt.close()

        if report:
            print('Classification Report')
            print(classification_report(y_true, y_pred))

    Y_pred = model.predict(X_test)
    y_pred = np.argmax(Y_pred, axis=1)
    print_confusion_matrix(y_test, y_pred)

    # --- Save final Keras model ---
    model.save(model_save_path, include_optimizer=False)
    print(f"Keras model saved to: {model_save_path}")

    # --- Convert to TFLite ---
    converter = tf.lite.TFLiteConverter.from_keras_model(model)
    converter.optimizations = [tf.lite.Optimize.DEFAULT]
    tflite_quantized_model = converter.convert()
    with open(tflite_save_path, 'wb') as f:
        f.write(tflite_quantized_model)
    print(f"TFLite model saved to: {tflite_save_path}")

    print("Training completed successfully.")

# Optional: allow running directly with environment variables (for testing)
if __name__ == "__main__":
    label_file = os.environ.get("LABEL_CSV")
    dataset_file = os.environ.get("KEYPOINT_CSV")

    if not label_file or not dataset_file:
        print("Error: LABEL_CSV and KEYPOINT_CSV environment variables must be set.")
        sys.exit(1)

    run_training(label_file, dataset_file)
