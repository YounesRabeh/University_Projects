import tkinter as tk
from tkinter import ttk
import random

def move_tile(row, col):
    global empty_row, empty_col
    if (row == empty_row and abs(col - empty_col) == 1) or \
       (col == empty_col and abs(row - empty_row) == 1):
        buttons[empty_row][empty_col].config(text=buttons[row][col].cget("text"), style="My.TButton")
        buttons[row][col].config(text="", style="Empty.TButton")
        empty_row, empty_col = row, col
        check_win()

def check_win():
    global buttons
    current_order = [int(buttons[i][j].cget("text")) if buttons[i][j].cget("text") != "" else 0 for i in range(4) for j in range(4)]
    if current_order == list(range(1, 16)):
        tk.messagebox.showinfo(":)", "Hai vinto")
        reset_game()

def reset_game():
    global buttons, empty_row, empty_col
    numbers = list(range(1, 16))
    random.shuffle(numbers)
    for i in range(4):
        for j in range(4):
            if numbers:
                num = numbers.pop()
                buttons[i][j].config(text=str(num), style="My.TButton")
            else:
                buttons[i][j].config(text="", style="Empty.TButton")
                empty_row, empty_col = i, j

root = tk.Tk()
root.title("15 merda")

# Set minimum size
root.minsize(600, 600)

# Configure the root window to be resizable
root.resizable(True, True)

# Define styles
style = ttk.Style()
style.configure("My.TButton", font=('Helvetica', '12', 'bold'), width=4, height=2)
style.configure("Empty.TButton", background="grey", width=4, height=2)

buttons = [[None]*4 for _ in range(4)]
empty_row, empty_col = 3, 3

for i in range(4):
    for j in range(4):
        button = ttk.Button(root, text="", style="Empty.TButton",
                           command=lambda row=i, col=j: move_tile(row, col))
        button.grid(row=i, column=j, padx=2, pady=2, sticky="nsew")
        buttons[i][j] = button

reset_button = ttk.Button(root, text="Reset Game", command=reset_game)
reset_button.grid(row=4, column=1, columnspan=2, pady=5)

reset_game()

# Configure grid weights for resizing
for i in range(4):
    root.grid_rowconfigure(i, weight=1)
    root.grid_columnconfigure(i, weight=1)

root.mainloop()
