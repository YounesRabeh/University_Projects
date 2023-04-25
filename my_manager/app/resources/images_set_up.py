import pathlib
import os.path

play_button_icon = "PlayButton.png"
pause_button_icon = "PauseButton.png"
reset_button_icon = "ResetButton.png"
logo_icon = "MyLogo.png"

current_dir = pathlib.Path(__file__).parent.resolve()

play_button_icon_abs_path = os.path.join(current_dir, play_button_icon)
pause_button_icon_abs_path = os.path.join(current_dir, pause_button_icon)
reset_button_icon_abs_path = os.path.join(current_dir, reset_button_icon)
logo_icon_abs_path = os.path.join(current_dir, logo_icon)
