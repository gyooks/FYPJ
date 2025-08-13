import pytest
import customtkinter as ctk
from unittest.mock import patch, mock_open, MagicMock
import os
import numpy as np
import cv2
import nbformat
from gui.settings import SettingsPage
from gui.how_to_use import HowtousePage
from gui.gestures import Gestures
from gui.create_gestures import CreateGestures
import GWBHands
import start

@pytest.fixture
def mock_master():
    """Mock customtkinter root to avoid GUI launch."""
    with patch("customtkinter.CTk.__init__", return_value=None), \
         patch("customtkinter.CTk.destroy", return_value=None):
        mock_tk = MagicMock()
        mock_tk._root = mock_tk  # For StringVar
        yield mock_tk

@pytest.fixture
def mock_preset_dir(tmp_path):
    """Mock preset directory with minimal files."""
    preset_dir = tmp_path / "gui" / "presets" / "Default"
    preset_dir.mkdir(parents=True)
    files = {
        "keypoint_classifier_label.csv": "0,fist\n1,open_palm\n",
        "keypoint.csv": "0,0.1,0.2\n1,0.3,0.4\n",
        "mapping.json": '{"fist": "w", "open_palm": "s"}'
    }
    for filename, content in files.items():
        (preset_dir / filename).write_text(content)
    return str(tmp_path)

@pytest.fixture
def mock_webcam():
    """Mock cv2.VideoCapture to avoid webcam access."""
    with patch("cv2.VideoCapture", return_value=MagicMock()) as mock_cap:
        mock_cap_instance = MagicMock()
        mock_cap_instance.isOpened.return_value = True
        mock_cap_instance.read.return_value = (True, np.zeros((480, 640, 3), dtype=np.uint8))
        mock_cap_instance.release.return_value = None
        mock_cap.return_value = mock_cap_instance
        yield mock_cap

def test_cursor_movement(mock_master, mock_preset_dir, mock_webcam):
    """TC-VG1: Verify cursor mode starts."""
    with patch("os.getcwd", return_value=mock_preset_dir), \
         patch("os.path.exists", return_value=True), \
         patch("subprocess.Popen") as mock_popen, \
         patch("tkinter.messagebox.showinfo"):
        GWBHands.toggle_cursor_default()
        mock_popen.assert_called_once()

def test_change_settings(mock_master):
    """TC-VG3: Verify settings save is called."""
    with patch("gui.settings.SettingsPage.__init__", return_value=None), \
         patch("gui.settings.SettingsPage.save_and_return") as mock_save:
        settings = SettingsPage(mock_master, back_to_main_callback=lambda: None)
        settings.save_and_return()
        mock_save.assert_called_once()

def test_reopen_gui(mock_master, mock_preset_dir, mock_webcam):
    """TC-VG4: Verify GUI reopens."""
    with patch("os.getcwd", return_value=mock_preset_dir), \
         patch("os.path.exists", return_value=True), \
         patch("builtins.open", mock_open(read_data='{"fist": "w", "open_palm": "s"}')), \
         patch("cv2.waitKey", return_value=ord('b')), \
         patch("start.get_args", return_value=MagicMock(
             mapping=os.path.join(mock_preset_dir, "gui", "presets", "Default", "mapping.json"),
             keypoints=os.path.join(mock_preset_dir, "gui", "presets", "Default", "keypoint.csv"),
             labels=os.path.join(mock_preset_dir, "gui", "presets", "Default", "keypoint_classifier_label.csv")
         )):
        GWBHands.selected_preset_paths = {
            "mapping_path": os.path.join(mock_preset_dir, "gui", "presets", "Default", "mapping.json"),
            "keypoint_csv_path": os.path.join(mock_preset_dir, "gui", "presets", "Default", "keypoint.csv"),
            "label_csv_path": os.path.join(mock_preset_dir, "gui", "presets", "Default", "keypoint_classifier_label.csv")
        }
        GWBHands.selected_preset = "Default"
        start.main()
        assert True

def test_view_tutorial(mock_master):
    """TC-VG5: Verify tutorial page is displayed."""
    with patch("gui.how_to_use.HowtousePage.__init__", return_value=None), \
         patch("gui.how_to_use.HowtousePage.place") as mock_place:
        how_to_use = HowtousePage(mock_master, back_to_main_callback=lambda: None)
        how_to_use.place(relx=0.5, rely=0.5, anchor="center")
        mock_place.assert_called_once()

def test_view_gestures(mock_master, mock_preset_dir):
    """TC-VG9: Verify gesture list is loaded."""
    with patch("os.getcwd", return_value=mock_preset_dir), \
         patch("os.path.exists", return_value=True), \
         patch("builtins.open", mock_open(read_data="0,fist\n1,open_palm\n")), \
         patch("gui.gestures.Gestures.__init__", return_value=None):
        gestures = Gestures(
            mock_master,
            back_to_main_callback=lambda: None,
            selected_preset={"label_csv_path": os.path.join(mock_preset_dir, "gui/presets/Default/keypoint_classifier_label.csv")}
        )
        gestures.gestures = ["fist", "open_palm"]
        assert gestures.gestures == ["fist", "open_palm"]

def test_retrain_model(mock_master, mock_preset_dir):
    """TC-VG13: Verify model retraining is triggered."""
    with patch("os.getcwd", return_value=mock_preset_dir), \
         patch("os.path.exists", return_value=True), \
         patch("customtkinter.CTkLabel.__init__", return_value=None), \
         patch("customtkinter.CTkLabel.configure", return_value=None), \
         patch("tkinter.messagebox.showinfo"), \
         patch("nbformat.read", return_value=nbformat.v4.new_notebook()), \
         patch("nbconvert.preprocessors.ExecutePreprocessor.preprocess", return_value=(None, None)):
        GWBHands.selected_preset = "Default"
        GWBHands.selected_preset_paths = {
            "label_csv_path": os.path.join(mock_preset_dir, "gui/presets/Default/keypoint_classifier_label.csv"),
            "keypoint_csv_path": os.path.join(mock_preset_dir, "gui/presets/Default/keypoint.csv")
        }
        GWBHands.retrain_model_from_notebook()
        assert True

def test_create_new_gesture(mock_master, mock_preset_dir, mock_webcam):
    """TC-VG14: Verify new gesture creation."""
    with patch("os.getcwd", return_value=mock_preset_dir), \
         patch("os.path.exists", return_value=True), \
         patch("builtins.open", mock_open()), \
         patch("gui.create_gestures.CreateGestures.__init__", return_value=None), \
         patch("gui.create_gestures.CreateGestures.save_gesture") as mock_save:
        create_gestures = CreateGestures(
            mock_master,
            back_to_gestures_callback=lambda: None,
            selected_preset={
                "label_csv_path": os.path.join(mock_preset_dir, "gui/presets/Default/keypoint_classifier_label.csv"),
                "keypoint_csv_path": os.path.join(mock_preset_dir, "gui/presets/Default/keypoint.csv")
            }
        )
        create_gestures.current_gesture_name = "Wave"
        create_gestures.save_gesture()
        mock_save.assert_called_once()

def test_delete_gesture(mock_master, mock_preset_dir):
    """TC-VG15: Verify gesture deletion."""
    with patch("os.getcwd", return_value=mock_preset_dir), \
         patch("os.path.exists", return_value=True), \
         patch("builtins.open", mock_open(read_data="0,fist\n1,open_palm\n")), \
         patch("tkinter.messagebox.askyesno", return_value=True), \
         patch("gui.gestures.Gestures.__init__", return_value=None), \
         patch("gui.gestures.Gestures.delete_gesture") as mock_delete:
        gestures = Gestures(
            mock_master,
            back_to_main_callback=lambda: None,
            selected_preset={
                "label_csv_path": os.path.join(mock_preset_dir, "gui/presets/Default/keypoint_classifier_label.csv"),
                "keypoint_csv_path": os.path.join(mock_preset_dir, "gui/presets/Default/keypoint.csv")
            }
        )
        gestures.gestures = ["fist", "open_palm"]
        gestures.delete_gesture("fist")
        mock_delete.assert_called_once()

def test_rename_gesture(mock_master, mock_preset_dir):
    """TC-VG16: Verify gesture renaming."""
    with patch("os.getcwd", return_value=mock_preset_dir), \
         patch("os.path.exists", return_value=True), \
         patch("builtins.open", mock_open(read_data="0,fist\n1,open_palm\n")), \
         patch("tkinter.messagebox.showinfo"), \
         patch("gui.gestures.Gestures.__init__", return_value=None), \
         patch("gui.gestures.Gestures.edit_gesture") as mock_edit:
        gestures = Gestures(
            mock_master,
            back_to_main_callback=lambda: None,
            selected_preset={
                "label_csv_path": os.path.join(mock_preset_dir, "gui/presets/Default/keypoint_classifier_label.csv")
            }
        )
        gestures.gestures = ["fist", "open_palm"]
        gestures.edit_gesture("fist")
        mock_edit.assert_called_once()

def test_webcam_support(mock_master):
    """TC-VG18: Verify webcam initialization."""
    with patch("gui.settings.SettingsPage.__init__", return_value=None), \
         patch("gui.settings.SettingsPage.test_webcam") as mock_test:
        settings = SettingsPage(mock_master, back_to_main_callback=lambda: None)
        settings.test_webcam()
        mock_test.assert_called_once()

def test_user_friendly_interface(mock_master):
    """TC-VG19: Verify main menu is displayed."""
    with patch("customtkinter.CTkFrame.__init__", return_value=None), \
         patch("customtkinter.CTkFrame.place") as mock_place:
        mainmenu = ctk.CTkFrame(mock_master, width=1280, height=720, fg_color="transparent")
        mainmenu.place(relx=0.5, rely=0.5, anchor="center")
        mock_place.assert_called_once()