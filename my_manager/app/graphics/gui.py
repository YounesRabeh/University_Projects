import tkinter as tk
from tkinter import ttk
from app.resources.images_set_up import play_button_icon_abs_path as play_btn_path, \
    pause_button_icon_abs_path as pause_btn_path, reset_button_icon_abs_path as reset_btn_path, \
    logo_icon_abs_path as logo_icon_path

from PIL import ImageTk, Image
import time
from data.file_os_manager import notification_call
import textwrap

# Default values FHD:
WINDOW_WIDTH = 1066
WINDOW_HEIGHT = 600
SCALE_FACTOR = 1


# Public data

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
        print(get_screen_size())
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
    color = '#024EE7'
    color_2 = 'WHITE'
    number_of_task = 1
    empty_default_space = " " * 80 + "\n\n"

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        ###############################
        self.color = '#024EE7'
        self.color_2 = 'WHITE'
        self.color_3 = 'Black'

        style = ttk.Style()
        style.map("TCombobox")
        style.configure("TCombobox", selectforeground=self.color_3, selectbackground=self.color_2)

        tk.Frame.configure(self, bg=self.color)
        # UI:
        self.checkbutton_list = ToDoPage.CheckbuttonList(self)
        self.delete_button = ttk.Button(self, text='Delete Checked',
                                        command=lambda: self.checkbutton_list.delete_checked_checkbutton())
        self.print_button = ttk.Button(self, text='Print values',
                                       command=self.checkbutton_list.print_checkbutton_values)
        self.task_name_entry = tk.Entry(self, width=26 * SCALE_FACTOR, font='Helvetica 20 bold')
        self.task_name_entry.insert(0, "TaskName")
        self.add_new_task = tk.Button(self, text='ADD TASK', width=9 * SCALE_FACTOR, font='Helvetica 12 bold',
                                      relief='groove', command=lambda: add_task())
        self.description_label = tk.Label(self, text="Task Description:", font='Helvetica 15 bold', bg=ToDoPage.color,
                                          fg=ToDoPage.color_2)
        self.task_description_entry = tk.Text(self, width=53 * SCALE_FACTOR, height=6, font='Helvetica 13')
        self.importance_level_label = tk.Label(self, text="Importance ", font='Helvetica 15 bold', bg=ToDoPage.color,
                                               fg=ToDoPage.color_2)
        self.importance_level_input = tk.StringVar()
        self.importance_list = ["None", "Low", "Medium", "High"]
        self.high_importance_combo = ttk.Combobox(self, textvariable=self.importance_level_input,
                                                  values=self.importance_list)
        self.high_importance_combo.current(0)
        self.high_importance_combo.config(state='readonly', style="TCombobox")

        # UI LAYOUT:
        self.delete_button.place(x=600, y=500)
        self.print_button.place(x=800, y=500)
        self.task_name_entry.place(x=int(WINDOW_WIDTH / 1.615 * SCALE_FACTOR), y=int(WINDOW_HEIGHT / 15 * SCALE_FACTOR),
                                   anchor='center')
        self.add_new_task.place(x=int(WINDOW_WIDTH / 1.077 * SCALE_FACTOR), y=int(WINDOW_HEIGHT / 15 * SCALE_FACTOR),
                                anchor='center')
        self.description_label.place(x=int(WINDOW_WIDTH / 2.085 * SCALE_FACTOR),
                                     y=int(WINDOW_HEIGHT / 5 * SCALE_FACTOR),
                                     anchor='center')
        self.task_description_entry.place(x=int(WINDOW_WIDTH / 1.455 * SCALE_FACTOR),
                                          y=int(WINDOW_HEIGHT / 2.5 * SCALE_FACTOR),
                                          anchor='center')
        self.importance_level_label.place(x=int(WINDOW_WIDTH / 2.2 * SCALE_FACTOR),
                                          y=int(WINDOW_HEIGHT / 1.65 * SCALE_FACTOR),
                                          anchor='center')
        self.high_importance_combo.place(x=int(WINDOW_WIDTH / 1.6 * SCALE_FACTOR),
                                         y=int(WINDOW_HEIGHT / 1.65 * SCALE_FACTOR),
                                         anchor='center')

        def add_task():
            checkbutton_frame = ToDoPage.CheckbuttonFrame(self.checkbutton_list.inner_frame,
                                                          get_title(),
                                                          get_description(),
                                                          ToDoPage.number_of_task,
                                                          get_importance(self.importance_level_input.get()))

            self.checkbutton_list.checkbutton_frames.append(checkbutton_frame)
            checkbutton_frame.draw()
            ToDoPage.number_of_task += 1
            self.task_name_entry.delete(0, tk.END)
            self.task_name_entry.insert(0, f"TaskName")
            self.task_description_entry.delete('1.0', tk.END)
            self.checkbutton_list.draw()

        def get_importance(input):
            if input == "High":
                return "RED"
            elif input == "Medium":
                return "ORANGE"
            elif input == "Low":
                return "GREEN"
            else:
                return "GRAY"

        def get_title(every=37):
            return textwrap.fill(self.task_name_entry.get(), every)

        def get_description():
            my_text = textwrap.fill(self.task_description_entry.get('1.0', tk.END), 40)
            return my_text

    class CheckbuttonFrame:
        def __init__(self, parent, title, sub_label, frame_number, importance):
            self.parent = parent
            self.count = 0
            self.importance_level = importance
            self.var = tk.BooleanVar()
            self.frame_number = frame_number
            self.frame = tk.Frame(parent, relief='solid', borderwidth=5)
            self.checkbutton = ttk.Checkbutton(self.frame, variable=self.var)
            self.label = tk.Label(self.frame, text=title)
            self.sub_label = tk.Label(self.frame, text=sub_label)
            self.importance_level_label = tk.Label(self.frame, text="    \n" * 2, bg=self.importance_level)

            self.checkbutton.grid(row=0, column=0, sticky='nw', padx=8, pady=2)
            self.importance_level_label.grid(row=1, column=0, sticky='nw')
            self.label.grid(row=0, column=1, sticky='w')
            self.sub_label.grid(row=1, column=1, rowspan=4,sticky='w')

        def draw(self):
            self.frame.pack(padx=5, pady=5, fill=tk.BOTH)

        def update(self):
            self.count += 1

            self.after(1000, self.update)

    class CheckbuttonList:
        def __init__(self, parent):
            self.checkbutton_frames = []
            self.count = 0
            self.parent = parent
            self.scroll_frame = ttk.Frame(parent)
            self.scroll_frame.pack(fill=tk.Y, expand=True, side=tk.LEFT, anchor="nw")
            self.canvas = tk.Canvas(self.scroll_frame, bg=ToDoPage.color_2)
            self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, anchor="nw")
            self.scrollbar = ttk.Scrollbar(self.scroll_frame, orient=tk.VERTICAL, command=self.canvas.yview)
            self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y, anchor="e")
            self.canvas.configure(yscrollcommand=self.scrollbar.set)
            self.inner_frame = ttk.Frame(self.canvas)
            self.canvas.create_window((0, 0), window=self.inner_frame, anchor='nw')

            for i in range(ToDoPage.number_of_task):
                checkbutton_frame = ToDoPage.CheckbuttonFrame(self.inner_frame, "Task Name (example)",
                                                              "The task description .... " + " " * 36, 0, "gray")
                self.checkbutton_frames.append(checkbutton_frame)
                checkbutton_frame.checkbutton.config(state='disable')
            self.draw()

        def draw(self):
            for checkbutton_frame in self.checkbutton_frames:
                checkbutton_frame.draw()
            self.canvas.update_idletasks()
            self.canvas.config(scrollregion=self.canvas.bbox('all'))

        def delete_checked_checkbutton(self):
            new_frames = []
            for checkbutton_frame in self.checkbutton_frames:
                if not checkbutton_frame.var.get():
                    new_frames.append(checkbutton_frame)
                else:
                    checkbutton_frame.frame.pack_forget()
            self.checkbutton_frames = new_frames
            self.frame_number_update()
            self.draw()

        def frame_number_update(self):
            counter = 0
            for checkbutton_frame in self.checkbutton_frames:
                checkbutton_frame.frame_number = counter
                counter += 1

        def print_checkbutton_values(self):
            for checkbutton_frame in self.checkbutton_frames:
                print(f"Check button {checkbutton_frame.frame_number} value: {checkbutton_frame.var.get()}")
            print("-"*27)

        def update(self):
            self.count += 1
            self.canvas.configure(yscrollcommand=self.scrollbar.set)
            #self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, anchor="nw")
            #self.canvas.create_window((0, 0), window=self.inner_frame, anchor='nw')

            #self.scroll_frame.pack(fill=tk.Y, expand=True, side=tk.LEFT, anchor="nw")

            self.after(1000, self.update)


# Driver Code
app = TkinterApp()
app.mainloop()
