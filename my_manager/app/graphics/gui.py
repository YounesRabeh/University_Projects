import tkinter as tk
from tkinter import ttk

class TkinterApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        # __init__ function for class Tk
        tk.Tk.__init__(self, *args, **kwargs)

        # creating a container
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (ToDoPage, TimerPage):
            frame = F(container, self)
            # initializing frame of that object from, TimerPage respectively with the for loop
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame(ToDoPage)

    def show_frame(self, cont):
        """To display the current frame passed as parameter"""
        frame = self.frames[cont]
        frame.tkraise()

# METHODS:
# default values FHD
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
def setup(_app):
    global SCREEN_WIDTH
    global SCREEN_HEIGHT
    SCREEN_WIDTH = _app.winfo_screenwidth()
    SCREEN_HEIGHT = _app.winfo_screenheight()

    def get_screen_size():
        """
        Get the parameter for the geometry function, big as half the screen
        and positioned in the lower side of the screen
        :return: The string "withxheight+position"
        """
        return str(int(SCREEN_WIDTH / 1.8)) + "x" + str(int(SCREEN_HEIGHT / 1.8)) + \
            "+" + str(int(SCREEN_WIDTH / 4.8)) + "+" + str(int(SCREEN_HEIGHT / 3.8))

    _app.geometry(get_screen_size())
    _app.title("My Manager --test")

# PAGES:
class ToDoPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        ###############################

        label = ttk.Label(self, text="To-Do Page")
        label.grid(row=0, column=4, padx=10, pady=10)

        button1 = ttk.Button(self, text="Timer Page",
                             command=lambda: controller.show_frame(TimerPage))
        button1.grid(row=1, column=1, padx=10, pady=10)


class TimerPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        ###############################

        label = ttk.Label(self, text="Timer Page")
        label.grid(row=0, column=4, padx=10, pady=10)

        button1 = ttk.Button(self, text="To-Do Page",
                             command=lambda: controller.show_frame(ToDoPage))
        button1.grid(row=1, column=1, padx=10, pady=10)


# Driver Code
app = TkinterApp()
setup(app)
app.mainloop()
