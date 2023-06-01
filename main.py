# EXTERNAL PACKAGES:
# GUI lib for Python - "tkinter"
import tkinter as tk
from tkinter.messagebox import askyesno

# To create plot/plots
import matplotlib
# To change style of plots
from matplotlib import style
# To create Figure and add axes on it
from matplotlib.figure import Figure
# To create FigureCanvas and grid the Figure as tk widget
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg # , NavigationToolbar2TkAgg
import matplotlib.pyplot as plt #TODO: check do I need it
# S: I have made additional installations:
#  sudo apt-get install python3-pill.imagetk
#  sudo pip install ipython

# INTERNAL PACKAGES:
import AnimationApp


# S: Some settings as shown on: 
# "How to add a Matplotlib Graph to Tkinter Window in Python 3 - Tkinter tutorial Python 3.4 p. 6"
# https://www.youtube.com/watch?v=Zw6M-BnAPP0&list=PLQVvvaa0QuDclKx-QpC9wntnURXVJqLyk&index=6
matplotlib.use("TkAgg")

LARGE_FONT = ("Verdana", 12)
style.use("ggplot")  # ggplot, dark_background

fig = Figure(tight_layout=True, dpi=100,)  # figsize=(9, 6), tight_layout=True
# S: add_subplot(rows, cols, index_of_this_subplot)
axs0 = fig.add_subplot(311)
axs1 = fig.add_subplot(312)
axs2 = fig.add_subplot(313)
axs = [axs0, axs1, axs2]

axs[0].set_title("Thermocouple tc0")
axs[1].set_title("Thermocouple tc1")
axs[2].set_title("Thermocouple tc2")

axs[0].set_ylabel("T, deg C")
axs[1].set_ylabel("T, deg C")
axs[2].set_ylabel("T, deg C")

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
        for F in (MainPageGUI,):
            frame = F(master=container, controller=self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew", )
            frame.grid_rowconfigure(0, weight=1)
            frame.grid_columnconfigure(0, weight=1)

        self.show_frame(MainPageGUI)

        # S: This variable MUST be at the end of this __init__()
        self.animationApp = AnimationApp.AnimationApp(fig, axs, self)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

class MainPageGUI(tk.Frame):
    def __init__(self, master, controller):
        tk.Frame.__init__(self, master=master)

        self.grid_rowconfigure(index=0, weight=0)
        self.grid_rowconfigure(index=1, weight=1)
        self.grid_rowconfigure(index=2, weight=1)
        self.grid_rowconfigure(index=3, weight=1)
        self.grid_rowconfigure(index=4, weight=0)
        self.grid_rowconfigure(index=5, weight=0)
        self.grid_rowconfigure(index=6, weight=0)
        self.grid_rowconfigure(index=7, weight=0)

        self.grid_columnconfigure(index=0, weight=0)
        self.grid_columnconfigure(index=1, weight=1)

        # 0.Frame for name of the experiment (and name of the file to write data in)////
        frame_entry_name_of_experiment = tk.Frame(master=self,
                                                  borderwidth=5, relief="groove")
        frame_entry_name_of_experiment.grid(
            row=0, column=0, columnspan=2, sticky="ew", padx=5, pady=5)
        frame_entry_name_of_experiment.grid_rowconfigure(index=0, weight=0)
        frame_entry_name_of_experiment.grid_columnconfigure(index=0, weight=1)
        frame_entry_name_of_experiment.grid_columnconfigure(index=1, weight=1)

        # Entry "Name of the experiment"
        label_entry_name_of_experiment = tk.Label(master=frame_entry_name_of_experiment,
                                                  text="Name of the experiment:", font=LARGE_FONT,
                                                  anchor="e")
        label_entry_name_of_experiment.grid(row=0, column=0)  # sticky="ew"s
        entry_name_of_experiment = tk.Entry(master=frame_entry_name_of_experiment,
                                            width=60, font=LARGE_FONT)
        entry_name_of_experiment.grid(row=0, column=1, sticky="ew", pady=5)

        # text = controller.animationApp.get_name_of_file()
        # entry_name_of_experiment.insert(0, text)
        # /////////////////////////////////////////////////////////////////////////

        # 
        # 1. Frame "Sample settings" //////////////////////////////////////////////
        frame_sample_settings = tk.Frame(master=self,
                                         borderwidth=5, relief="groove")
        frame_sample_settings.grid(
            row=1, column=0, sticky="nsew", padx=5, pady=5)

        frame_sample_settings.grid_rowconfigure(index=0, weight=0)
        frame_sample_settings.grid_rowconfigure(index=1, weight=0)

        frame_sample_settings.grid_columnconfigure(index=0, weight=1)
        frame_sample_settings.grid_columnconfigure(index=1, weight=0)

        # Lable "Sample settings"
        label_sample_settings = tk.Label(master=frame_sample_settings,
                                         text="Sample settings:", font=LARGE_FONT,
                                         anchor="w")
        label_sample_settings.grid(row=0, column=0, columnspan=2, sticky="ew")

        # Entry "Height of the sample"
        label_entry_h = tk.Label(master=frame_sample_settings,
                                 text="Height, mm:", font=LARGE_FONT,
                                 anchor="e")
        label_entry_h.grid(row=1, column=0, sticky="ew")
        entry_h = tk.Entry(master=frame_sample_settings,
                           width=10, font=LARGE_FONT)
        entry_h.grid(row=1, column=1, sticky="e", padx=5)
        # /////////////////////////////////////////////////////////////////////////

        # 2. Frame "Experiment settings"///////////////////////////////////////////
        frame_experiment_settings = tk.Frame(master=self,
                                             borderwidth=5, relief="groove")
        frame_experiment_settings.grid(
            row=2, column=0, sticky="nsew", padx=5, pady=5)

        frame_experiment_settings.grid_rowconfigure(index=0, weight=0)
        frame_experiment_settings.grid_rowconfigure(index=1, weight=0)
        frame_experiment_settings.grid_rowconfigure(index=2, weight=0)

        frame_experiment_settings.grid_columnconfigure(index=0, weight=1)
        frame_experiment_settings.grid_columnconfigure(index=1, weight=0)

        # Lable "Experiment settings"
        label_experiment_settings = tk.Label(anchor="w", master=frame_experiment_settings,
                                             text="Experiment settings:", font=LARGE_FONT)
        label_experiment_settings.grid(
            row=0, column=0, columnspan=2, sticky="ew")

        # Entry "Quantity of measurements"
        label_quantity_of_measurements = tk.Label(master=frame_experiment_settings,
                                                  text="Quantity of experiments:", font=LARGE_FONT,
                                                  anchor="e")
        label_quantity_of_measurements.grid(row=1, column=0, sticky="ew")
        entry_quantity_of_measurements = tk.Entry(master=frame_experiment_settings,
                                                  width=10, font=LARGE_FONT)
        entry_quantity_of_measurements.grid(row=1, column=1, sticky="ew")

        # Entry "Delay between measurements"
        label_delay_between_measurements = tk.Label(master=frame_experiment_settings,
                                                    text="Delay between measurements:", font=LARGE_FONT,
                                                    anchor="e")
        label_delay_between_measurements.grid(row=2, column=0, sticky="ew")
        entry_delay_between_measurements = tk.Entry(master=frame_experiment_settings,
                                                    width=10, font=LARGE_FONT)
        entry_delay_between_measurements.grid(row=2, column=1, sticky="ew")
        # /////////////////////////////////////////////////////////////////////////

        # 3. Frame "Experiment results"////////////////////////////////////////////
        frame_experiment_results = tk.Frame(master=self,
                                            borderwidth=5, relief="groove")
        frame_experiment_results.grid(
            row=3, column=0, sticky="nsew", padx=5, pady=5)

        frame_experiment_results.grid_rowconfigure(index=0, weight=0)
        frame_experiment_results.grid_rowconfigure(index=1, weight=0)
        # frame_experiment_results.grid_rowconfigure(index=2, weight=0)

        frame_experiment_results.grid_columnconfigure(index=0, weight=1)
        frame_experiment_results.grid_columnconfigure(index=1, weight=0)

        # Lable "Experiment results"
        label_experiment_results = tk.Label(master=frame_experiment_results,
                                     text="Experiment results:", font=LARGE_FONT,
                                     anchor="e")
        label_experiment_results.grid(row=0, column=0, columnspan=2, sticky="ew")

        # Entry "Some result"
        label_some_result = tk.Label(master=frame_experiment_results,
                                     text="Some result:", font=LARGE_FONT,
                                     anchor="e")
        label_some_result.grid(row=1, column=0, sticky="ew")
        entry_some_result = tk.Entry(master=frame_experiment_results,
                                     width=10, font=LARGE_FONT)
        entry_some_result.grid(row=1, column=1, sticky="ew")
        # /////////////////////////////////////////////////////////////////////////

        # 2.2. Right column with plots
        self.canvas = FigureCanvasTkAgg(figure=fig, master=self)
        self.canvas.draw()
        self.canvas.get_tk_widget().grid(row=1, rowspan=3, column=1,
                                         sticky="nsew", padx=5, pady=5)

        # Buttons
        button_start_animation = tk.Button(master=self,
                                           text="Start Animation", font=LARGE_FONT,
                                           command=lambda: controller.animationApp.start())
        button_start_animation.grid(row=4, column=0, columnspan=2, sticky="nsew", padx=5, pady=5)

        button_pause_animation = tk.Button(master=self,
                                           text="Pause Animation", font=LARGE_FONT,
                                           command=lambda: controller.animationApp.pause())
        button_pause_animation.grid(row=5, column=0, columnspan=2, sticky="nsew", padx=5, pady=5)

        button_resume_animation = tk.Button(master=self,
                                            text="Resume Animation", font=LARGE_FONT,
                                            command=lambda: controller.animationApp.resume())
        button_resume_animation.grid(row=6, column=0, columnspan=2, sticky="nsew", padx=5, pady=5)

        button_finish_animation = tk.Button(master=self,
                                            text="Finish Animation", font=LARGE_FONT,
                                            command=lambda: controller.animationApp.finish())
        button_finish_animation.grid(row=7, column=0, columnspan=2, sticky="nsew", padx=5, pady=5)

        print("Page Three is initted")

def confirm(root):
    answer = askyesno(title='Exit', message='Do You Want To Exit?')
    if answer:
        root.data_reader.close()
        print("Serial is closed from confirm()")
        root.destroy()


app = MyApp()

app.mainloop()
