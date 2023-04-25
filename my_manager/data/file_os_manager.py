from plyer import notification
from app.resources.images_set_up import logo_icon_abs_path
import numpy as np
import pathlib
import os.path

# OS:
current_dir = pathlib.Path(__file__).parent.resolve()
DATA_file_abs_path = os.path.join(current_dir, "DATA.txt")


# Info:
data_marker = "&"*7
frame_marker = "\n" + "%"*10
frame_data_array = np.array(["", "", ""])


def save_task_data(_title, _description, _importance):
    _data_file = open(DATA_file_abs_path, "a")
    _data_file.write(_title + data_marker + _description + data_marker + _importance + frame_marker)
    _data_file.close()

def get_stored_data():
    global DATA_FILE
    line_counter = 0
    _data_file = open(DATA_file_abs_path, "r")

    for current_line in _data_file:
        current_line = current_line.replace(frame_marker, "")
        current_line = current_line.replace("%%%%%%%%%%", "")
        current_line = current_line.replace(data_marker, "\n", 2)

        end_of_index = current_line.find("\n")
        title = current_line[0:end_of_index]
        current_line = current_line[end_of_index+1:]

        end_of_index = current_line.find("\n")
        description = current_line[0:end_of_index]
        current_line = current_line[end_of_index + 1:]

        end_of_index = current_line.find("\n")
        importance = current_line[0:end_of_index]
        #single_data_array = np.array([title, description, importance])
        DATA_FILE[line_counter][0] = title
        DATA_FILE[line_counter][1] = description
        DATA_FILE[line_counter][2] = importance
        line_counter += 1
    _data_file.close()

def delete_data(line_number):
    global DATA_FILE

    with open(DATA_file_abs_path, "r") as file:
        lines = file.readlines()
    del lines[line_number]

    with open(DATA_file_abs_path, "w") as file:
        file.writelines(lines)



def number_of_lines(file):
    count = 0
    for line in file:
        if line != "\n":
            count += 1
    return count

def notification_call(_title, _message):
    notification.notify(
        title=_title,
        message=_message,
        app_icon=logo_icon_abs_path,
        timeout=5,
        toast=False
    )

NUMBER_OF_LINES = number_of_lines(open(DATA_file_abs_path, "r"))
DATA_FILE = [[None, None, None] for i in range(NUMBER_OF_LINES)]
get_stored_data()
