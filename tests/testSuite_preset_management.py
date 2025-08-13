import pytest
import customtkinter as ctk
from unittest.mock import patch, mock_open, MagicMock, ANY
import os
import json
import shutil
from gui.change_preset import ChangePreset
from gui.create_preset import CreatePreset
from gui.edit_preset import EditPreset

@pytest.fixture
def mock_master():
    return ctk.CTk()

@pytest.fixture
def mock_preset_dir(tmp_path):
    # Create presets and gui/presets to match application expectation
    preset_dir = tmp_path / "presets"
    preset_dir.mkdir()
    default_dir = preset_dir / "Default"
    default_dir.mkdir()
    gui_preset_dir = tmp_path / "gui" / "presets" / "Default"
    gui_preset_dir.mkdir(parents=True)
    files = {
        "keypoint_classifier_label.csv": "fist\nopen_palm\n",
        "keypoint.csv": "0,0.1,0.2\n1,0.3,0.4\n",
        "mapping.json": '{"fist": "w", "open_palm": "s"}'
    }
    for filename, content in files.items():
        (default_dir / filename).write_text(content)
        (gui_preset_dir / filename).write_text(content)
    return str(tmp_path)  # Return tmp_path, not preset_dir

def test_view_active_preset(mock_master, mock_preset_dir):
    """TC-VG2: Verify active preset is displayed (manual file system interaction)."""
    with patch("os.getcwd", return_value=mock_preset_dir):
        preset = ChangePreset(mock_master, back_to_main_callback=lambda: None)
        assert "Default" in preset.presets_dict
        assert preset.presets_dict["Default"] == {"fist": "w", "open_palm": "s"}

def test_change_current_preset(mock_master, mock_preset_dir):
    """TC-VG6: Verify switching presets updates active preset (manual file system)."""
    with patch("os.getcwd", return_value=mock_preset_dir), \
         patch("gui.edit_preset.EditPreset.load_gestures", return_value=["fist", "open_palm"]):
        preset = ChangePreset(mock_master, back_to_main_callback=lambda: None, update_preset_callback=MagicMock())
        preset.use_preset("Default")
        preset.update_preset_callback.assert_called_with("Default", {
            "mapping_path": os.path.join(mock_preset_dir, "gui", "presets", "Default", "mapping.json"),
            "keypoint_csv_path": os.path.join(mock_preset_dir, "gui", "presets", "Default", "keypoint.csv"),
            "label_csv_path": os.path.join(mock_preset_dir, "gui", "presets", "Default", "keypoint_classifier_label.csv")
        })

def test_delete_preset(mock_master, mock_preset_dir):
    """TC-VG7: Verify preset deletion calls folder removal (mocked for safety)."""
    with patch("os.getcwd", return_value=mock_preset_dir), \
         patch("gui.edit_preset.EditPreset.load_gestures", return_value=["fist", "open_palm"]), \
         patch("shutil.rmtree") as mock_rmtree:
        preset = ChangePreset(mock_master, back_to_main_callback=lambda: None)
        preset.delete_preset("Default")
        mock_rmtree.assert_called_with(os.path.join(mock_preset_dir, "gui", "presets", "Default"))

def test_create_new_preset(mock_master, mock_preset_dir):
    """TC-VG8: Verify new preset creation copies files and saves mapping (manual file system)."""
    with patch("tkinter.messagebox.showinfo") as mock_showinfo, \
         patch("gui.edit_preset.EditPreset.load_gestures", return_value=["fist", "open_palm"]):
        create_preset = CreatePreset(
            mock_master,
            gesture_csv_path=os.path.join(mock_preset_dir, "gui", "presets", "Default", "keypoint_classifier_label.csv"),
            save_dir=os.path.join(mock_preset_dir, "gui", "presets"),
            back_callback=lambda: None,
            update_presets_callback=lambda: None
        )
        create_preset.preset_name.set("NewPreset")
        create_preset.mapping_rows = [(ctk.StringVar(value="fist"), ctk.StringVar(value="w"))]
        create_preset.save_preset()
        # Verify folder and files were created
        new_preset_dir = os.path.join(mock_preset_dir, "gui", "presets", "NewPreset")
        assert os.path.exists(new_preset_dir)
        assert os.path.exists(os.path.join(new_preset_dir, "mapping.json"))
        assert os.path.exists(os.path.join(new_preset_dir, "keypoint.csv"))
        assert os.path.exists(os.path.join(new_preset_dir, "keypoint_classifier_label.csv"))
        with open(os.path.join(new_preset_dir, "mapping.json"), "r", encoding="utf-8") as f:
            mapping = json.load(f)
            assert mapping == {"fist": "w"}
        mock_showinfo.assert_called_with("Success", "Preset 'NewPreset' created successfully.")

def test_map_keybind_to_gesture(mock_master, mock_preset_dir):
    """TC-VG10: Verify mapping keybind to gesture in preset (mocked for GUI)."""
    with patch("os.path.exists", return_value=True), \
         patch("builtins.open", mock_open(read_data='{"fist": "w"}')), \
         patch("gui.edit_preset.EditPreset.load_gestures", return_value=["fist", "open_palm"]), \
         patch("gui.edit_preset.EditPreset.load_existing_mapping", return_value={"fist": "w"}):
        edit_preset = EditPreset(
            mock_master,
            preset_name="Default",
            preset_dir=os.path.join(mock_preset_dir, "gui", "presets", "Default"),
            back_callback=lambda: None,
            update_callback=lambda: None
        )
        edit_preset.mapping_rows = [(ctk.StringVar(value="open_palm"), ctk.StringVar(value="s"), MagicMock())]
        with patch("json.dump") as mock_dump:
            edit_preset.save_changes()
            mock_dump.assert_called_with({"open_palm": "s"}, ANY, indent=4)

def test_edit_existing_keybind(mock_master, mock_preset_dir):
    """TC-VG11: Verify editing keybind updates mapping (mocked for GUI)."""
    with patch("os.path.exists", return_value=True), \
         patch("builtins.open", mock_open(read_data='{"fist": "w"}')), \
         patch("gui.edit_preset.EditPreset.load_gestures", return_value=["fist", "open_palm"]), \
         patch("gui.edit_preset.EditPreset.load_existing_mapping", return_value={"fist": "w"}):
        edit_preset = EditPreset(
            mock_master,
            preset_name="Default",
            preset_dir=os.path.join(mock_preset_dir, "gui", "presets", "Default"),
            back_callback=lambda: None,
            update_callback=lambda: None
        )
        edit_preset.mapping_rows[0][1].set("a")  # Change key to 'a'
        with patch("json.dump") as mock_dump:
            edit_preset.save_changes()
            mock_dump.assert_called_with({"fist": "a"}, ANY, indent=4)