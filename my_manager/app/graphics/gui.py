import tkinter as tk
from tkinter import ttk
from resources.images_set_up import play_button_icon_abs_path as play_btn_path,\
    pause_button_icon_abs_path as pause_btn_path, reset_button_icon_abs_path as reset_btn_path
from PIL import ImageTk, Image

# Default values FHD:
WINDOW_WIDTH = 1066
WINDOW_HEIGHT = 600
SCALE_FACTOR = 1

class TkinterApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        # __init__ function for class Tk
        tk.Tk.__init__(self, *args, **kwargs)
        global WINDOW_WIDTH
        global WINDOW_HEIGHT
        global SCALE_FACTOR
        SCREEN_WIDTH = self.winfo_screenwidth()
        SCREEN_HEIGHT = self.winfo_screenheight()
        WINDOW_WIDTH = int(SCREEN_WIDTH / 1.8)
        WINDOW_HEIGHT = int(SCREEN_HEIGHT / 1.8)
        SCALE_FACTOR = self.scale_factor()
        self.data = 8

        # creating a container
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        def get_screen_size():
            """
            Get the parameter for the geometry function, big as half the screen
            and positioned in the lower side of the screen
            :return: The string "withxheight+position"
            """
            return str(WINDOW_WIDTH) + "x" + str(WINDOW_HEIGHT) + \
                "+" + str(int(SCREEN_WIDTH / 4.8)) + "+" + str(int(SCREEN_HEIGHT / 3.8))

        # Window Settings:
        self.geometry(get_screen_size())
        self.title("My Manager --test")
        self.resizable(width=False, height=False)

        # Images:
        icon_size = int(100 * SCALE_FACTOR)
        self.play_button_icon = ImageTk.PhotoImage((Image.open(play_btn_path)).resize((icon_size, icon_size)))
        self.pause_button_icon = ImageTk.PhotoImage((Image.open(pause_btn_path)).resize((icon_size+9, icon_size+9)))
        self.reset_button_icon = ImageTk.PhotoImage(Image.open(reset_btn_path).resize((icon_size, icon_size)))

        # Menu(toolbar):
        menubar = tk.Menu(self)
        self.config(menu=menubar, relief='ridge')
        new_menu = tk.Menu(menubar, tearoff=0, relief='ridge')
        new_menu.add_command(label="Timer", command=lambda: self.show_frame(TimerPage))
        new_menu.add_command(label="Countdown", command=lambda: self.show_frame(CountdownPage))
        new_menu.add_command(label="TO-DO", command=lambda: self.show_frame(ToDoPage))
        new_menu.add_separator()
        new_menu.add_command(label="Exit", command=lambda: self.destroy())
        menubar.add_cascade(label="File", menu=new_menu)

        # Frames Manager:
        self.frames = {}
        self.my_frames = [TimerPage, CountdownPage, ToDoPage]
        for F in self.my_frames:
            frame = F(container, self)
            # initializing frame of that object from, TimerPage respectively with the for loop
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame(TimerPage)

    def scale_factor(self):
        # TODO: make a function that returns the correct scale factor for every screen size
        return 1

    def show_frame(self, cont):
        """To display the current frame passed as parameter"""
        frame = self.frames[cont]
        frame.tkraise()


# METHODS:

# PAGES:
class TimerPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.seconds = 0
        self.is_running = False
        ###############################

        self.color = 'YELLOW'
        tk.Frame.configure(self, bg=self.color)
        # UI:
        self.time_label = ttk.Label(self, text="00:00:00", background=self.color,
                                    font=("Arial", int(150*SCALE_FACTOR)))
        self.start_button = tk.Button(self, text="START", command=lambda: start_timer(), bg=self.color, fg=self.color,
                                      activebackground=self.color, highlightcolor=self.color, bd=0,
                                      image=controller.play_button_icon, highlightthickness=0)
        self.reset_button = tk.Button(self, text="RESET", command=lambda: reset_timer(),bg=self.color, fg=self.color,
                                      activebackground=self.color, highlightcolor=self.color, bd=0,
                                      image=controller.reset_button_icon, highlightthickness=0)

        print(controller.data)
        # UI LAYOUT:
        self.time_label.place(x=int(WINDOW_WIDTH/2*SCALE_FACTOR), y=int(WINDOW_HEIGHT/3*SCALE_FACTOR),
                              anchor='center')
        self.start_button.place(x=int(WINDOW_WIDTH/2.8*SCALE_FACTOR), y=int(WINDOW_HEIGHT/1.3*SCALE_FACTOR),
                                anchor='center')
        self.reset_button.place(x=int(WINDOW_WIDTH/1.7*SCALE_FACTOR), y=int(WINDOW_HEIGHT/1.3*SCALE_FACTOR),
                                anchor='center')

        # OWN METHODS:
        def start_timer():
            self.is_running = True
            self.start_button.config(command=pause_timer, image=controller.pause_button_icon)
            update_clock()

        def pause_timer():
            self.is_running = False
            print(controller.play_button_icon)
            self.start_button.config(command=start_timer, image=controller.play_button_icon)

        def reset_timer():
            self.seconds = 0
            self.is_running = False
            self.start_button.config(command=start_timer, image=controller.play_button_icon)
            self.time_label.config(text="00:00:00")

        def update_clock():
            if self.is_running:
                self.seconds += 1
                hours = self.seconds // 3600
                minutes = (self.seconds % 3600) // 60
                secs = self.seconds % 60
                time_string = "{:02d}:{:02d}:{:02d}".format(hours, minutes, secs)
                self.time_label.config(text=time_string)
                if self.seconds == 0:
                    return
                controller.after(1000, update_clock)  # call update_clock again after 1000 ms


class CountdownPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        ###############################
        self.color = 'RED'

        tk.Frame.configure(self, bg=self.color)
        # UI:
        self.time_label = ttk.Label(self, text="00:00:00", background=self.color,
                                    font=("Arial", int(150*SCALE_FACTOR)))
        self.start_button = tk.Button(self, text="START", command=lambda: ...,
                                      width=int(15*SCALE_FACTOR), height=int(6*SCALE_FACTOR))
        self.reset_button = tk.Button(self, text="RESET", command=lambda: ...,
                                      width=int(15*SCALE_FACTOR), height=int(6*SCALE_FACTOR))

        # UI LAYOUT:
        self.time_label.place(x=int(WINDOW_WIDTH/2*SCALE_FACTOR), y=int(WINDOW_HEIGHT/3*SCALE_FACTOR),
                             anchor='center')
        self.start_button.place(x=int(WINDOW_WIDTH/2.8*SCALE_FACTOR), y=int(WINDOW_HEIGHT/1.3*SCALE_FACTOR),
                                anchor='center')
        self.reset_button.place(x=int(WINDOW_WIDTH/1.7*SCALE_FACTOR), y=int(WINDOW_HEIGHT/1.3*SCALE_FACTOR),
                                anchor='center')


class ToDoPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        ###############################
        self.color = 'BLUE'

        tk.Frame.configure(self, bg=self.color)
        label = ttk.Label(self, text="To-Do Page")
        label.grid(row=0, column=1, padx=10, pady=10)

# Driver Code
app = TkinterApp()
app.mainloop()
