import tkinter as tk
from tkinter import ttk
from app.resources.images_set_up import play_button_icon_abs_path as play_btn_path, \
    pause_button_icon_abs_path as pause_btn_path, reset_button_icon_abs_path as reset_btn_path, \
    logo_icon_abs_path as logo_icon_path

from PIL import ImageTk, Image
import time
from data.file_os_manager import notification_call

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

        # Images:
        icon_size = int(100 * SCALE_FACTOR)
        self.play_button_icon = ImageTk.PhotoImage((Image.open(play_btn_path)).resize((icon_size, icon_size)))
        self.pause_button_icon = ImageTk.PhotoImage((Image.open(pause_btn_path)).resize((icon_size + 9, icon_size + 9)))
        self.reset_button_icon = ImageTk.PhotoImage(Image.open(reset_btn_path).resize((icon_size, icon_size)))
        self.logo_icon = ImageTk.PhotoImage(Image.open(logo_icon_path))

        # Window Settings:
        self.geometry(get_screen_size())
        self.title("My Manager --test")
        self.resizable(width=False, height=False)
        self.wm_iconphoto(False, self.logo_icon)

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
        self.show_frame(ToDoPage)

    def scale_factor(self):
        # TODO: make a function that returns the correct scale factor for every screen size
        return 1

    def show_frame(self, cont):
        """To display the current frame passed as parameter"""
        frame = self.frames[cont]
        frame.tkraise()


# PAGES:
class TimerPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.hours, self.minutes, self.seconds = 0, 0, 0
        self.total_elapsed_time = 0
        self.last_start_time = None
        self.paused = False
        ###############################
        self.color = '#13D45A'

        tk.Frame.configure(self, bg=self.color)
        # UI:
        self.time_label = ttk.Label(self, text="00:00:00", background=self.color,
                                    font=("Arial", int(150 * SCALE_FACTOR)))
        self.start_button = tk.Button(self, command=lambda: start_pause(), bg=self.color, fg=self.color,
                                      activebackground=self.color, highlightcolor=self.color, bd=0,
                                      image=controller.play_button_icon, highlightthickness=0)
        self.reset_button = tk.Button(self, command=lambda: reset(), bg=self.color, fg=self.color,
                                      activebackground=self.color, highlightcolor=self.color, bd=0,
                                      image=controller.reset_button_icon, highlightthickness=0)

        # UI LAYOUT:
        self.time_label.place(x=int(WINDOW_WIDTH / 2 * SCALE_FACTOR), y=int(WINDOW_HEIGHT / 2.5 * SCALE_FACTOR),
                              anchor='center')
        self.start_button.place(x=int(WINDOW_WIDTH / 2.8 * SCALE_FACTOR), y=int(WINDOW_HEIGHT / 1.3 * SCALE_FACTOR),
                                anchor='center')
        self.reset_button.place(x=int(WINDOW_WIDTH / 1.7 * SCALE_FACTOR), y=int(WINDOW_HEIGHT / 1.3 * SCALE_FACTOR),
                                anchor='center')

        # OWN METHODS:
        def tick():
            if self.last_start_time is not None and not self.paused:
                current_elapsed_time = round(time.time() - self.last_start_time) + self.total_elapsed_time
                self.seconds = current_elapsed_time % 60
                self.minutes = (current_elapsed_time // 60) % 60
                self.hours = current_elapsed_time // 3600
                time_string = f"{self.hours:02d}:{self.minutes:02d}:{self.seconds:02d}"
                self.time_label.config(text=time_string)
            self.master.after(1000, tick)

        def start_pause():
            if self.last_start_time is None:
                self.last_start_time = time.time()
                tick()
                self.start_button.config(image=controller.pause_button_icon)
            elif not self.paused:
                self.total_elapsed_time += round(time.time() - self.last_start_time)
                self.paused = True
                self.start_button.config(image=controller.play_button_icon)
            else:
                self.last_start_time = time.time()
                self.paused = False
                self.start_button.config(image=controller.pause_button_icon)

        def reset():
            self.hours, self.minutes, self.seconds, self.total_elapsed_time = 0, 0, 0, 0
            self.paused = False
            self.start_button.config(image=controller.play_button_icon)
            self.time_label.config(text="00:00:00")
            self.last_start_time = None


class CountdownPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.hours, self.minutes, self.seconds = 0, 0, 0
        self.current_time, self.total_time = 0, 0
        self.is_running = False
        self.input_seconds = tk.StringVar()
        self.input_minutes = tk.StringVar()
        self.input_hours = tk.StringVar()
        self.one_to_sixty = []
        self.one_to_twenty_four = []
        for x in range(60):
            if x < 10:
                self.one_to_sixty.append("0" + str(x))
            else:
                self.one_to_sixty.append(x)
        for x in range(24):
            if x < 10:
                self.one_to_twenty_four.append("0" + str(x))
            else:
                self.one_to_twenty_four.append(x)
        self.last_start_time = None
        self.pause_start_time = None
        self.total_elapsed_time = 0
        ###############################
        self.color = '#DE2222'
        self.color_2 = 'white'
        self.color_3 = 'black'

        tk.Frame.configure(self, bg=self.color)
        # UI:
        self.time_label = ttk.Label(self, text="00:00:00", background=self.color,
                                    font=("Arial", int(150 * SCALE_FACTOR)))
        self.start_button = tk.Button(self, command=lambda: start_pause(), bg=self.color, fg=self.color,
                                      activebackground=self.color, highlightcolor=self.color, bd=0,
                                      image=controller.play_button_icon, highlightthickness=0)
        self.reset_button = tk.Button(self, command=lambda: reset(), bg=self.color, fg=self.color,
                                      activebackground=self.color, highlightcolor=self.color, bd=0,
                                      image=controller.reset_button_icon, highlightthickness=0)
        self.text_label = tk.Label(self, text="To change the starting time, RESET to take effect",
                                   font='Helvetica 12', bg=self.color, fg=self.color_2)

        self.style = ttk.Style()
        self.style.theme_create('combo_style', parent='alt',
                                settings={'TCombobox':
                                              {'configure':
                                                   {'selectbackground': self.color_3,
                                                    'fieldbackground': self.color_2,
                                                    'background': self.color_2,
                                                    }}})
        self.style.theme_use('combo_style')
        self.seconds_combobox = ttk.Combobox(self, textvariable=self.input_seconds, state='readonly',
                                             values=self.one_to_sixty, font='Helvetica 30 bold', width=2)
        self.minutes_combobox = ttk.Combobox(self, textvariable=self.input_minutes, state='readonly',
                                             values=self.one_to_sixty, font='Helvetica 30 bold', width=2)
        self.hour_combobox = ttk.Combobox(self, textvariable=self.input_hours, state='readonly',
                                          values=self.one_to_twenty_four, font='Helvetica 30 bold', width=2)
        self.seconds_combobox.current(0)
        self.minutes_combobox.current(0)
        self.hour_combobox.current(0)

        # UI LAYOUT:
        self.time_label.place(x=int(WINDOW_WIDTH / 2 * SCALE_FACTOR), y=int(WINDOW_HEIGHT / 2.5 * SCALE_FACTOR),
                              anchor='center')
        self.start_button.place(x=int(WINDOW_WIDTH / 2.8 * SCALE_FACTOR), y=int(WINDOW_HEIGHT / 1.3 * SCALE_FACTOR),
                                anchor='center')
        self.reset_button.place(x=int(WINDOW_WIDTH / 1.7 * SCALE_FACTOR), y=int(WINDOW_HEIGHT / 1.3 * SCALE_FACTOR),
                                anchor='center')
        self.seconds_combobox.place(x=int(WINDOW_WIDTH / 1.2 * SCALE_FACTOR), y=int(WINDOW_HEIGHT / 9 * SCALE_FACTOR),
                                    anchor='center')
        self.minutes_combobox.place(x=int(WINDOW_WIDTH / 2 * SCALE_FACTOR), y=int(WINDOW_HEIGHT / 9 * SCALE_FACTOR),
                                    anchor='center')
        self.hour_combobox.place(x=int(WINDOW_WIDTH / 5.7 * SCALE_FACTOR), y=int(WINDOW_HEIGHT / 9 * SCALE_FACTOR),
                                 anchor='center')
        self.text_label.place(x=int(WINDOW_WIDTH / 1.27 * SCALE_FACTOR), y=int(WINDOW_HEIGHT / 1.05 * SCALE_FACTOR),
                              anchor='center')

        # OWN METHODS:
        def get_time():
            self.hours = int(self.hour_combobox.get())
            self.minutes = int(self.minutes_combobox.get())
            self.seconds = int(self.input_seconds.get())

        self.x = 0

        def start_pause():
            if (self.current_time == 0) or self.x == 0:
                get_time()

                self.total_time = self.hours * 3600 + self.minutes * 60 + self.seconds
                self.current_time = self.total_time
                time_string = f"{self.hours:02d}:{self.minutes:02d}:{self.seconds:02d}"
                self.time_label.config(text=time_string)
            self.x += 1
            if not self.is_running:
                self.is_running = True
                self.start_button.config(image=controller.pause_button_icon)
                self.last_start_time = time.time()
                countdown()
            else:
                self.is_running = False
                self.start_button.config(image=controller.play_button_icon)
                self.total_elapsed_time += round(time.time() - self.last_start_time)

        def countdown():
            if self.is_running and self.current_time > 0:
                self.current_time = self.total_time - round(
                    time.time() - self.last_start_time) - self.total_elapsed_time
                hours = self.current_time // 3600
                minutes = (self.current_time // 60) % 60
                seconds = self.current_time % 60
                self.time_label.config(text='{:02d}:{:02d}:{:02d}'.format(hours, minutes, seconds))
                self.master.after(100, countdown)
            elif self.current_time <= 0:
                self.time_label.config(text='00:00:00')
                self.is_running = False
                self.start_button.config(image=controller.play_button_icon)
                notification_call("COUNTDOWN DONE !", "Go check the App")

        def reset():
            get_time()
            self.is_running = False
            self.start_button.config(image=controller.play_button_icon)
            self.current_time = self.total_time
            self.time_label.config(text='{:02d}:{:02d}:{:02d}'.format(self.hours, self.minutes, self.seconds))
            self.last_start_time = None
            self.pause_start_time = None
            self.total_elapsed_time = 0
            self.x = 0


class ToDoPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        ###############################
        self.color = 'BLUE'

        tk.Frame.configure(self, bg=self.color)
        # UI:
        checkbutton_list = ToDoPage.CheckbuttonList(self)
        delete_button = ttk.Button(self, text='Delete Checked', command=checkbutton_list.delete_checked_checkbuttons)
        print_button = ttk.Button(self, text='Print values', command=checkbutton_list.print_checkbutton_values)

        # UI LAYOUT:
        delete_button.pack(side=tk.RIGHT, padx=10, pady=10)
        print_button.pack(side=tk.RIGHT, padx=10, pady=10)

    class CheckbuttonFrame:
        def __init__(self, parent, title, sub_label, frame_number):
            self.parent = parent
            self.var = tk.BooleanVar()
            self.frame_number = frame_number
            self.frame = ttk.Frame(parent, relief='solid', borderwidth=5,)
            self.checkbutton = ttk.Checkbutton(self.frame, variable=self.var)
            self.label = ttk.Label(self.frame, text=title)
            self.sub_label = ttk.Label(self.frame, text=sub_label)
            self.checkbutton.grid(row=0, column=0, sticky='nw', padx=8, pady=2)
            self.label.grid(row=0, column=1, sticky='w')
            self.sub_label.grid(row=1, column=1, sticky='w')

        def draw(self):
            self.frame.pack(padx=5, pady=5, fill=tk.BOTH)

    class CheckbuttonList:
        def __init__(self, parent):
            self.parent = parent
            self.scroll_frame = ttk.Frame(parent)
            self.scroll_frame.pack(fill=tk.Y, expand=True, side=tk.LEFT, anchor="nw")
            self.canvas = tk.Canvas(self.scroll_frame, bg='white')
            self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, anchor="nw")
            self.scrollbar = ttk.Scrollbar(self.scroll_frame, orient=tk.VERTICAL, command=self.canvas.yview)
            self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y, anchor="e")
            self.canvas.configure(yscrollcommand=self.scrollbar.set)
            self.inner_frame = ttk.Frame(self.canvas)
            self.canvas.create_window((0, 0), window=self.inner_frame, anchor='nw')
            self.checkbutton_frames = []
            self.empty_default_space = " " * 80 + "\n\n"

            for i in range(20):
                checkbutton_frame = ToDoPage.CheckbuttonFrame(self.inner_frame, self.set_title() + str(i + 1),
                                                              self.empty_default_space, i + 1)
                self.checkbutton_frames.append(checkbutton_frame)
            self.draw()

        def draw(self):
            for checkbutton_frame in self.checkbutton_frames:
                checkbutton_frame.draw()
            self.canvas.update_idletasks()
            self.canvas.config(scrollregion=self.canvas.bbox('all'))

        def delete_checked_checkbuttons(self):
            new_frames = []
            for checkbutton_frame in self.checkbutton_frames:
                if not checkbutton_frame.var.get():
                    new_frames.append(checkbutton_frame)
                else:
                    checkbutton_frame.frame.pack_forget()
            self.checkbutton_frames = new_frames
            self.draw()

        def print_checkbutton_values(self):
            for checkbutton_frame in self.checkbutton_frames:
                print(f"Check button {checkbutton_frame.frame_number} value: {checkbutton_frame.var.get()}")

        def set_title(self):
            return "Title"


# Driver Code
app = TkinterApp()
app.mainloop()
