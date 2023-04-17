 def tick(self):
        if self.last_start_time is not None and not self.paused:
            current_elapsed_time = round(time.time() - self.last_start_time) + self.total_elapsed_time
            self.seconds = current_elapsed_time % 60
            self.minutes = (current_elapsed_time // 60) % 60
            self.hours = current_elapsed_time // 3600
            time_string = f"{self.hours:02d}:{self.minutes:02d}:{self.seconds:02d}"
            self.time_label.config(text=time_string)
        self.master.after(1000, self.tick)

    def start_pause(self):
        if self.last_start_time is None:
            self.last_start_time = time.time()
            self.tick()
            self.start_pause_button.config(text="Pause")
        elif not self.paused:
            self.total_elapsed_time += round(time.time() - self.last_start_time)
            self.paused = True
            self.start_pause_button.config(text="Resume")
        else:
            self.last_start_time = time.time()
            self.paused = False
            self.start_pause_button.config(text="Pause")
