# lesson from youtube "Live Maplotlib Graph in Tkinter Window in Python3 - Tkinter tutorial Python 3.4p.7"
from tkinter.messagebox import askyesno
# , NavigationToolbar2TkAgg
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import DataReader
import AnimationApp
import time
import random
import serial
import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib import style
import matplotlib.animation as animation
from matplotlib.figure import Figure
import matplotlib
matplotlib.use("TkAgg")
# S: I have made additional installations:
#  sudo apt-get install python3-pill.imagetk
#  sudo pip install ipython


LARGE_FONT = ("Verdana", 12)
style.use("ggplot")  # ggplot, dark_background

# WAY2======================================================
# S: add_subplot(rows, cols, index_of_this_subplot)
fig = Figure(tight_layout=True, dpi=100,)  # figsize=(9, 6), tight_layout=True

axs0 = fig.add_subplot(311)
axs1 = fig.add_subplot(312)
axs2 = fig.add_subplot(313)
axs = [axs0, axs1, axs2]

# ===========================================================

axs[0].set_title("Thermocouple tc0")
axs[1].set_title("Thermocouple tc1")
axs[2].set_title("Thermocouple tc2")

axs[0].set_ylabel("T, deg C")
axs[1].set_ylabel("T, deg C")
axs[2].set_ylabel("T, deg C")


def confirm(root):
    answer = askyesno(title='Exit', message='Do You Want To Exit?')
    if answer:
        root.data_reader.close()
        print("Serial is closed from confirm()")
        root.destroy()


class MyApp(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        # tk.Tk.iconbitmap(self)
        tk.Tk.wm_title(self, "Thermal Conductivity Measurement Program")

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # S: Creatig several frames in one container.
        #    Details on the lesson "Multiple Windows/Frames in Tkinter GUI with Python - Tkinter tutorial Python 3.4 p. 4"
        #    https://www.youtube.com/watch?v=jBUpjijYtCk&list=PLQVvvaa0QuDclKx-QpC9wntnURXVJqLyk&index=4
        self.frames = {}
        for F in (PageThree,):
            frame = F(master=container, controller=self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew", )
            frame.grid_rowconfigure(0, weight=1)
            frame.grid_columnconfigure(0, weight=1)

        self.show_frame(PageThree)

        # S: This variable MUST be at the end of this __init__()
        self.animationApp = AnimationApp.AnimationApp(fig, axs, self)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


class PageThree(tk.Frame):
    def __init__(self, master, controller):
        tk.Frame.__init__(self, master=master)

        # 0. Frame main for all page
        frame_for_all_elements_on_the_page = tk.Frame(
            master=self, borderwidth=5, relief="groove")
        frame_for_all_elements_on_the_page.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        frame_for_all_elements_on_the_page.grid_columnconfigure(
            index=0, weight=1)
        frame_for_all_elements_on_the_page.grid_rowconfigure(index=0, weight=0)
        frame_for_all_elements_on_the_page.grid_rowconfigure(index=1, weight=1)
        frame_for_all_elements_on_the_page.grid_rowconfigure(index=2, weight=0)
        frame_for_all_elements_on_the_page.grid_rowconfigure(index=3, weight=0)
        frame_for_all_elements_on_the_page.grid_rowconfigure(index=4, weight=0)

        # 1.Frame for name of the experiment (and name of the file to write data in)
        frame_entry_name_of_experiment = tk.Frame(master=frame_for_all_elements_on_the_page,
                                                  borderwidth=5, relief="groove")
        frame_entry_name_of_experiment.grid(
            row=0, column=0, sticky="ew", padx=5, pady=5)
        frame_entry_name_of_experiment.grid_columnconfigure(index=0, weight=1)
        frame_entry_name_of_experiment.grid_columnconfigure(index=1, weight=1)
        frame_entry_name_of_experiment.grid_rowconfigure(index=0, weight=0)

        label_entry_name_of_experiment = tk.Label(master=frame_entry_name_of_experiment,
                                                  text="Name of the experiment:", font=LARGE_FONT,
                                                  anchor="w")
        label_entry_name_of_experiment.grid(row=0, column=0, sticky="ew")

        entry_name_of_experiment = tk.Entry(
            frame_entry_name_of_experiment, width=60, font=LARGE_FONT)
        entry_name_of_experiment.grid(row=0, column=1, sticky="ew")
        # text = controller.animationApp.get_name_of_file()
        # entry_name_of_experiment.insert(0, text)
        # ------------------------------------------------------------------------

        # 2. Frame for main part of the page
        frame_main = tk.Frame(master=frame_for_all_elements_on_the_page,
                              borderwidth=5, relief="sunken")
        frame_main.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
        frame_main.grid_rowconfigure(index=0, weight=1)
        frame_main.grid_rowconfigure(index=1, weight=1)
        frame_main.grid_rowconfigure(index=2, weight=1)
        frame_main.grid_columnconfigure(index=0, weight=1)
        frame_main.grid_columnconfigure(index=1, weight=1)

        # 2.1. Left Column Frame with input (entries) and output (lables) fields
        frame_in_and_out = tk.Frame(master=frame_main,
                                    borderwidth=5, relief="groove")
        frame_in_and_out.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        frame_in_and_out.grid_rowconfigure(index=0, weight=1)
        frame_in_and_out.grid_rowconfigure(index=1, weight=1)
        frame_in_and_out.grid_rowconfigure(index=2, weight=1)
        frame_in_and_out.grid_columnconfigure(index=0, weight=1)

        # 2.1.1. Frame and Lable "Sample settings"
        frame_sample_settings = tk.Frame(master=frame_main,
                                         borderwidth=5, relief="groove")
        frame_sample_settings.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        label_sample_settings = tk.Label(anchor="nw", master=frame_sample_settings,
                                         text="Sample settings:", font=LARGE_FONT)
        label_sample_settings.grid(row=0, column=0, sticky="nsew")

        # Lable and Entry "Height of the sample"
        label_entry_h = tk.Label(master=frame_sample_settings,
                                 text="Height:", font=LARGE_FONT,
                                 anchor="w")
        label_entry_h.grid(row=1, column=0)
        entry_h = tk.Entry(master=frame_sample_settings,
                           width=20, font=LARGE_FONT)
        entry_h.grid(row=1, column=1, sticky="w")

        # 2.1.2. Frame and Lable "Experiment Settings"
        frame_experiment_settings = tk.Frame(master=frame_main,
                                             borderwidth=5, relief="groove")
        frame_experiment_settings.grid(
            row=1, column=0, sticky="nsew", padx=5, pady=5)
        label_experiment_settings = tk.Label(anchor="nw", master=frame_experiment_settings,
                                             text="Experiment settings:", font=LARGE_FONT)
        label_experiment_settings.grid(row=0, column=0, sticky="nsew")

        # Lable and Entry "Quantity of measurements"
        label_quantity_of_measurements = tk.Label(master=frame_experiment_settings,
                                                  text="Quantity of experiments:", font=LARGE_FONT)
        label_quantity_of_measurements.grid(row=1, column=0, sticky="ns")
        entry_quantity_of_measurements = tk.Entry(master=frame_experiment_settings,
                                                  width=20, font=LARGE_FONT)
        entry_quantity_of_measurements.grid(row=1, column=1, sticky="ns")

        # Lable and Entry "Delay between measurements"
        label_delay_between_measurements = tk.Label(master=frame_experiment_settings,
                                                    text="Delay between measurements:", font=LARGE_FONT)
        label_delay_between_measurements.grid(row=2, column=0, sticky="ns")
        entry_delay_between_measurements = tk.Entry(master=frame_experiment_settings,
                                                    width=20, font=LARGE_FONT)
        entry_delay_between_measurements.grid(row=2, column=1, sticky="ns")

        # 2.2. Right column with plots
        
        self.canvas = FigureCanvasTkAgg(figure=fig, master=frame_main)
        self.canvas.draw()
        self.canvas.get_tk_widget().grid(column=1, row=0, rowspan=3, sticky="nsew", padx=10, pady=10)
        
        # Buttons
        button_start_animation = tk.Button(master=frame_for_all_elements_on_the_page,
                                           text="Start Animation", font=LARGE_FONT,
                                           command=lambda: controller.animationApp.start())
        button_start_animation.grid(row=2, column=0, sticky="nsew", padx=5, pady=5)

        button_pause_animation = tk.Button(master=frame_for_all_elements_on_the_page,
                                           text="Pause Animation", font=LARGE_FONT,
                                           command=lambda: controller.animationApp.pause())
        button_pause_animation.grid(row=3, column=0, sticky="nsew", padx=5, pady=5)

        button_resume_animation = tk.Button(master=frame_for_all_elements_on_the_page,
                                            text="Resume Animation", font=LARGE_FONT,
                                            command=lambda: controller.animationApp.resume())
        button_resume_animation.grid(row=4, column=0, sticky="nsew", padx=5, pady=5)

        button_finish_animation = tk.Button(master=frame_for_all_elements_on_the_page,
                                            text="Finish Animation", font=LARGE_FONT,
                                            command=lambda: controller.animationApp.finish())
        button_finish_animation.grid(row=5, column=0, sticky="nsew", padx=5, pady=5)

        print("Page Three is initted")


app = MyApp()

app.mainloop()
