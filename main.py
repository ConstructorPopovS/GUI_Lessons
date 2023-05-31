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
fig = Figure(figsize=(9, 6), tight_layout=True, dpi=100,) #figsize=(9, 6), tight_layout=True

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

        self.frames = {}
        for F in (StartPage, PageOne, PageTwo, PageThree):
            # for F in (PageThree):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(PageThree)

        # S: This variable MUST be at the end of this __init__()
        self.animationApp = AnimationApp.AnimationApp(fig, axs, self)


    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Start Page", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        button1 = tk.Button(self, text="Visit page One",
                            command=lambda: controller.show_frame(PageOne))
        button1.pack()

        button2 = tk.Button(self, text="Visit page Two",
                            command=lambda: controller.show_frame(PageTwo))
        button2.pack()

        button3 = tk.Button(self, text="Visit page Three",
                            command=lambda: controller.show_frame(PageThree))
        button3.pack()
        print("Start pade is initted")

class PageOne(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Page One", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        button1 = tk.Button(self, text="Back to Home",
                            command=lambda: controller.show_frame(StartPage))
        button1.pack()

        button2 = tk.Button(self, text="Visit page Two",
                            command=lambda: controller.show_frame(PageTwo))
        button2.pack()

        button3 = tk.Button(self, text="Visit page Three",
                            command=lambda: controller.show_frame(PageThree))
        button3.pack()
        print("Page One is initted")

class PageTwo(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Page Two!!!", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        button1 = tk.Button(self, text="Back to Home",
                            command=lambda: controller.show_frame(StartPage))
        button1.pack()

        button2 = tk.Button(self, text="Visit page One",
                            command=lambda: controller.show_frame(PageOne))
        button2.pack()

        button3 = tk.Button(self, text="Visit page Three",
                            command=lambda: controller.show_frame(PageThree))
        button3.pack()
        print("Page Two is initted")

class PageThree(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        # 1.Frame for name of the experiment (and name of the file to write data in)
        frame_entry_name_of_experiment = tk.Frame(
            self, borderwidth=5, relief="groove")
        frame_entry_name_of_experiment.pack(anchor="n", pady=5,
            side=tk.TOP, fill=tk.X, expand=True)
        
        label_entry_name_of_experiment = tk.Label(
            frame_entry_name_of_experiment, text="Name of the experiment:", font=LARGE_FONT)
        label_entry_name_of_experiment.grid(row=0, column=0, sticky="ew")

        entry_name_of_experiment = tk.Entry(
            frame_entry_name_of_experiment, width=60, font=LARGE_FONT)
        entry_name_of_experiment.grid(row=0, column=1, sticky="ew")
        # text = controller.animationApp.get_name_of_file()
        # entry_name_of_experiment.insert(0, text)
        # ------------------------------------------------------------------------
# 
        # 2. Frame for main part of the page
        frame_main = tk.Frame(self,  borderwidth=5, relief="sunken",
                              padx=5, pady=10)
        frame_main.pack(anchor="n", side=tk.TOP, fill=tk.BOTH, expand=True)
# 
        # 2.1. Frame for left column with input (entries) and output (lables) fields
        frame_in_and_out = tk.Frame(frame_main,  borderwidth=5, relief="groove",
                                    padx=5, pady=10)
        frame_in_and_out.grid(row=0, column=0, sticky="nsew")
# 
        # 2.1.1. Label "Sample settings"
        label_sample_settings = tk.Label(master=frame_in_and_out,
                                         text="Sample settings:", font=LARGE_FONT)
        label_sample_settings.grid(row=0, column=0, sticky="nsew")
# 
        # 2.1.2. Entry height of the sample
        label_entry_h = tk.Label(master=frame_in_and_out,
                                 text="Height of the sample:", font=LARGE_FONT)
        label_entry_h.grid(row=1, column=0, sticky="ns")
        entry_h = tk.Entry(master=frame_in_and_out, width=20, font=LARGE_FONT)
        entry_h.grid(row=1, column=1, sticky="ns")
# 
        # 2.1.3. Label "Sample settings"
        label_experiment_settings = tk.Label(master=frame_in_and_out,
                                             text="Experiment settings:", font=LARGE_FONT)
        label_experiment_settings.grid(row=2, column=0, sticky="nsew")
# 
        # 2.1.4. Entry number of measurements (Quantity)
        label_number_of_measurements = tk.Label(master=frame_in_and_out,
                                                text="Quantity of experiments:", font=LARGE_FONT)
        label_number_of_measurements.grid(row=3, column=0, sticky="ns")
        entry_number_of_measurements = tk.Entry(master=frame_in_and_out,
                                                width=20, font=LARGE_FONT)
        entry_number_of_measurements.grid(row=3, column=1, sticky="ns")
# 
        # 2.1.5. Entry delay between measurements
        label_delay_between_measurements = tk.Label(master=frame_in_and_out,
                                                    text="Delay between measurements:", font=LARGE_FONT)
        label_delay_between_measurements.grid(row=4, column=0, sticky="ns")
        entry_delay_between_measurements = tk.Entry(master=frame_in_and_out,
                                                    width=20, font=LARGE_FONT)
        entry_delay_between_measurements.grid(row=4, column=1, sticky="ns")
# 
        # 2.2. Right column with plots
        self.canvas = FigureCanvasTkAgg(fig, frame_main)
        self.canvas.draw()
        self.canvas.get_tk_widget().grid(row=0, column=1, sticky="nsew")
        # self.canvas.get_tk_widget().pack()
        
        # Buttons
        button_start_animation = tk.Button(self, text="Start Animation", font=LARGE_FONT,
                                           command=lambda: controller.animationApp.start())
        button_start_animation.pack()

        button_pause_animation = tk.Button(self, text="Pause Animation", font=LARGE_FONT,
                                           command=lambda: controller.animationApp.pause())
        button_pause_animation.pack()

        button_resume_animation = tk.Button(self, text="Resume Animation", font=LARGE_FONT,
                                            command=lambda: controller.animationApp.resume())
        button_resume_animation.pack()

        button_finish_animation = tk.Button(self, text="Finish Animation", font=LARGE_FONT,
                                            command=lambda: controller.animationApp.finish())
        button_finish_animation.pack()

        print("Page Three is initted")


app = MyApp()

app.mainloop()
# ser.close()
print("Serial is closed")
