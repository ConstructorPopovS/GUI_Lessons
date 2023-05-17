# lesson from youtube "Live Maplotlib Graph in Tkinter Window in Python3 - Tkinter tutorial Python 3.4p.7"
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg #, NavigationToolbar2TkAgg
# S: I have made additional installation:
#  sudo apt-get install python3-pill.imagetk
#  sudo pip install ipython


from matplotlib.figure import Figure
import matplotlib.animation as animation
from matplotlib import style

import tkinter as tk

import matplotlib.pyplot as plt
import numpy as np

import serial
import random

LARGE_FONT = ("Verdana", 18)
style.use("ggplot")# ggplot, dark_background

# fig_tc0 = Figure(figsize=(5,5), dpi=100)
# ax_tc0 = fig_tc0.add_subplot(111)



# A figure with three subplots
fig, axs = plt.subplots(3)
fig.set_figwidth(26)
fig.set_figheight(14)

x_List = []

y0_List = []
y1_List = []
y2_List = []

ser = serial.Serial(port='/dev/ttyACM0',baudrate=9600,timeout=15)


def animate(i,axs, x_List, y_List, ser, command_to_send_in_serial): 
    # command_to_send_in_serial should be in byte format: (a_tc, y_tc_List, b'command_to_send', ser)
    ser.write(command_to_send_in_serial)
    aData_str = ser.readline().decode('ascii')
    # aData_str = str(random.randrange(20,40))

    try:
        aData_float = float(aData_str)
        y_List.append(aData_float)
        print(command_to_send_in_serial.decode() + " = "+ str(aData_float))
        # TODO:Check append(i) in first time
        if (i > 0):
            if (x_List[-1] != i):
                x_List.append(i)

    except:
        print("UserExeption: convertation tc_str to float is failed")

    y_List = y_List[-10:]
    x_List = x_List[-10:]

    axs.clear()
    axs.plot(x_List,y_List) #xList,
    axs.set_ylim(15, 45)
    try:
        axs.set_xlim(x_List[-10], (x_List[-10] + 10))
    except:
        axs.set_xlim(0, 10)

    axs.set_title("Thermocouple " + command_to_send_in_serial.decode())
    axs.set_ylabel("Temperature, deg C")

def full_animation(i, axs0, axs1, axs2, x_List, y0_List, y1_List, y2_List, ser, ser_command0, ser_command1, ser_command2):
    animate(i, axs0, x_List, y0_List, ser, ser_command0)
    animate(i, axs1, x_List, y1_List, ser, ser_command1)
    animate(i, axs2, x_List, y2_List, ser, ser_command2)

def animate_all_plots(i,ser, x_List,
                      ax0, y0_List, ser_command0,
                      ax1, y1_List, ser_command1,
                      ax2, y2_List, ser_command2): 
    
    # command_to_send_in_serial should be in byte format: b'command_to_send'
    ser.write(ser_command0)
    y0_str = ser.readline().decode('ascii')

    ser.write(ser_command1)
    y1_str = ser.readline().decode('ascii')

    ser.write(ser_command2)
    y2_str = ser.readline().decode('ascii')

    
    # y0_str = str(random.randrange(20,40))
    # y1_str = str(random.randrange(18,35))
    # y2_str = str(random.randrange(15,25))

    try:
        y0_float = float(y0_str)
        y0_List.append(y0_float)
        print(ser_command0.decode() + " = "+ str(y0_float))

        y1_float = float(y1_str)
        y1_List.append(y1_float)
        print(ser_command0.decode() + " = "+ str(y1_float))
        
        y2_float = float(y2_str)
        y2_List.append(y2_float)
        print(ser_command0.decode() + " = "+ str(y2_float))
        print("=========================")

        x_List.append(i)

    except:
        print("UserExeption: convertation tc_str to float is failed")

    x_List = x_List[-10:]

    y0_List = y0_List[-10:]
    y1_List = y1_List[-10:]
    y2_List = y2_List[-10:]
    
    ax0.clear()
    ax0.plot(x_List,y0_List)
    ax0.set_ylim(10, 55)

    ax1.clear()
    ax1.plot(x_List,y1_List)
    # ax1.set_ylim(10, 55)

    ax2.clear()
    ax2.plot(x_List,y2_List)
    # ax2.set_ylim(10, 55)

    try:
        ax0.set_xlim(x_List[-10], (x_List[-10] + 10))
        ax1.set_xlim(x_List[-10], (x_List[-10] + 10))
        ax2.set_xlim(x_List[-10], (x_List[-10] + 10))
    except:
        ax0.set_xlim(0, 10)
        ax1.set_xlim(0, 10)
        ax2.set_xlim(0, 10)

    ax0.set_title("Thermocouple " + ser_command0.decode())
    ax0.set_ylabel("Temperature, deg C")

    ax1.set_title("Thermocouple " + ser_command1.decode())
    ax1.set_ylabel("Temperature, deg C")

    ax2.set_title("Thermocouple " + ser_command2.decode())
    ax2.set_ylabel("Temperature, deg C")

class MyApp(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        # tk.Tk.iconbitmap(self)
        tk.Tk.wm_title(self, "Th Con Program")

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
        label = tk.Label(self, text="Page One", font = LARGE_FONT)
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
        label = tk.Label(self, text="Page Two!!!", font = LARGE_FONT)
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
        label = tk.Label(self, text="Page Three", font = LARGE_FONT)
        label.pack(pady=10, padx=10)

        button1 = tk.Button(self, text="Back to Home",
                            command=lambda: controller.show_frame(StartPage))
        button1.pack()

        button2 = tk.Button(self, text="Visit page One",
                            command=lambda: controller.show_frame(PageOne))
        button2.pack()

        button3 = tk.Button(self, text="Visit page Two",
                            command=lambda: controller.show_frame(PageOne))
        button3.pack()
        
        canvas = FigureCanvasTkAgg(fig, self)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
 
        print("Page Three is initted")


app = MyApp()
MAX_FRAMES = 60
# ani_0 = animation.FuncAnimation(fig, animate, frames=100, fargs=(axs[0], x_List, y0_List, ser, b'tc0'), interval=1000) #, save_count=MAX_FRAMES

# ani_1 = animation.FuncAnimation(fig, full_animation, frames=100, fargs=(axs[0], axs[1], x_List, y0_List, y1_List, y2_List ser, b'tc0', b'tc1', b'tc2'), interval=1000) #, save_count=MAX_FRAMES

# ani = animation.FuncAnimation(fig, animate_all_plots, frames=100, fargs=(ser, x_List,
#                                                                          axs[0], y0_List, b'tc0',
#                                                                          axs[1], y1_List, b'tc1',
#                                                                          axs[2], y2_List, b'tc2',), interval=1000)
app.mainloop()
ser.close()
print("Serial is closed")


