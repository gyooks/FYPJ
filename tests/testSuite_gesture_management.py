import customtkinter as ctk
from gui.gestures import Gestures
from unittest.mock import mock_open, patch
import pytest

def test_delete_gesture_shows_message():
    # Mock CSV file content
    mock_csv_content = "fist,0\nother_gesture,1\n"
    mock_file = mock_open(read_data=mock_csv_content)

    # Mock file operations and os.path.exists
    with patch("builtins.open", mock_file), \
         patch("os.path.exists", return_value=True), \
         patch("os.path.isfile", return_value=True):  # Add isfile for extra safety
        master = ctk.CTk()
        gestures = Gestures(
            master,
            back_to_main_callback=lambda: None,
            selected_preset={"label_csv_path": "dummy.csv"}
        )
        gestures.gesture = ['fist']
        
        # Call delete_gesture and capture the message
        message = gestures.delete_gesture('fist')
        
        # Debug: Print the actual message if assertion fails
        print(f"Expected message: 'Gesture is deleted', Got: '{message}'")
        
        # Assert the expected message
        assert message == "Gesture is deleted", f"Unexpected message: {message}"

        # Verify file write operation
        mock_file().write.assert_called_once()
        written_content = mock_file().write.call_args[0][0]
        assert "fist" not in written_content, "Deleted gesture 'fist' still in CSV"