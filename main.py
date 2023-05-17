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

LARGE_FONT = ("Verdana", 18)
style.use("ggplot")# ggplot, dark_background

fig_tc0 = Figure(figsize=(5,5), dpi=100)
ax_tc0 = fig_tc0.add_subplot(111)
x_List = []
# xList.append(int(0))
y_tc0_List = []

# Some example data to display
x = np.linspace(0, 2*np.pi, 400)
y = np.sin(x**2)
# A figure with just one subplot
fig, ax = plt.subplots()
y_List = []
# ax.plot(x, y)
# ax.set_title("A single plot")

# A figure with two subplots
# fig_tc, ax_tc = plt.subplots(2)
# ax_tc[0].plot(x, y)
# ax_tc[1].plot(x, -y)
# ax_tc[0].set_title("The first plot")
# ax_tc[1].set_title("The second plot")

ser = serial.Serial('/dev/ttyACM0',9600)

def animate(i,axs, x_List, y_List, ser, command_to_send_in_serial): 
    # command_to_send_in_serial should be in byte format: (a_tc, y_tc_List, b'command_to_send', ser)
    ser.write(command_to_send_in_serial)
    arduinoData_string = ser.readline().decode('ascii')

    try:
        arduinoData_float = float(arduinoData_string)
        y_List.append(arduinoData_float)
        print(command_to_send_in_serial.decode() + " = "+ str(arduinoData_float))
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

def animate_tc(i,axs, y_List, command_to_send_in_serial, ser): 
    # command_to_send_in_serial should be in byte format: (a_tc, y_tc_List, b'command_to_send', ser)
    ser.write(command_to_send_in_serial)
    arduinoData_string = ser.readline().decode('ascii')

    try:
        arduinoData_float = float(arduinoData_string)
        y_List.append(arduinoData_float)
        print(command_to_send_in_serial.decode() + " = "+ str(arduinoData_float))
        # newX = xList[-1] + 1
        # x_List.append(i)

    except:
        print("UserExeption: convertation tc_str to float is failed")

    y_List = y_List[-10:]
    # x_List = x_List[-10:]

    axs.clear()
    axs.plot(y_List) #xList,
    axs.set_ylim(15, 45)
    axs.set_title("Thermocouple " + command_to_send_in_serial.decode())
    axs.set_ylabel("Temperature, deg C")
    
    
    # a_tc.clear()
    # a_tc.plot(y_tc_List) #xList,
    # a_tc.set_ylim(15, 45)
    # a_tc.set_title("Thermocouple " + command_to_send_in_serial.decode())
    # a_tc.set_ylabel("Temperature, deg C")


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
        print("Page Three init")
        
        canvas = FigureCanvasTkAgg(fig, self)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
 
        print("Page Three is initted")


app = MyApp()
MAX_FRAMES = 60
ani = animation.FuncAnimation(fig, animate, frames=100, fargs=(ax, x_List, y_List, ser, b'tc0'), interval=1000) #, save_count=MAX_FRAMES
app.mainloop()
ser.close()
print("Serial is closed")


