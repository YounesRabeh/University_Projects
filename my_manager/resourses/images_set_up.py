import pathlib
import os.path


play_button_icon = "PlayButton.png"
pause_button_icon = "PauseButton.png"
reset_button_icon = "ResetButton.png"

current_dir = pathlib.Path(__file__).parent.resolve()

play_button_icon_abs_path = os.path.join(current_dir, play_button_icon)
pause_button_icon_abs_path = os.path.join(current_dir, pause_button_icon)
reset_button_icon_abs_path = os.path.join(current_dir, reset_button_icon)

"""
print(pause_button_icon_abs_path)
print(path.exists(start_button_icon_abs_path), start_button_icon_abs_path)
my_path = '/home/YOUNES/Desktop/YOUNES/Python Projects/My Manager/resources/PlayButton.png'
print(path.exists(my_path), my_path)
"""

