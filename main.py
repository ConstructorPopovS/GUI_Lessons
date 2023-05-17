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
# from tkinter import tk

import serial

LARGE_FONT = ("Verdana", 18)
style.use("ggplot")# ggplot, dark_background

f_tc0 = Figure(figsize=(5,5), dpi=100)
f_tc1 = Figure(figsize=(5,5), dpi=100)

a_tc0 = f_tc0.add_subplot(111)
a_tc1 = f_tc1.add_subplot(111)

xList = []
xList.append(int(0))

y_tc0_List = []
y_tc1_List = []

ser = serial.Serial('/dev/ttyACM0',9600)

def animate_tc(i,a_tc, y_tc_List, command_to_send_in_serial, ser): 
    # command_to_send_in_serial should be in byte format: (a_tc, y_tc_List, b'command_to_send', ser)
    ser.write(command_to_send_in_serial)
    arduinoData_string = ser.readline().decode('ascii')

    try:
        arduinoData_float = float(arduinoData_string)
        y_tc0_List.append(arduinoData_float)
        print(command_to_send_in_serial.decode() + " = "+ str(arduinoData_float))
        # newX = xList[-1] + 1
        # xList.append(newX)

    except:
        print("UserExeption: convertation tc_str to float is failed")

    y_tc_List = y_tc_List[-10:]
    # xList = xList[-10:]
    
    a_tc.clear()
    a_tc.plot(y_tc_List) #xList,
    a_tc.set_ylim(15, 45)
    a_tc.set_title("Thermocouple " + command_to_send_in_serial.decode())
    a_tc.set_ylabel("Temperature, deg C")


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

        canvas_tc0 = FigureCanvasTkAgg(f_tc0, self)
        canvas_tc0.draw()
        canvas_tc0.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        canvas_tc1 = FigureCanvasTkAgg(f_tc1, self)
        canvas_tc1.draw()
        canvas_tc1.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        print("Page Three is initted")


app = MyApp()
MAX_FRAMES = 60
ani_tc0 = animation.FuncAnimation(f_tc0, animate_tc, frames=100, fargs=(a_tc0, y_tc0_List, b'tc0', ser), interval=1000) #, save_count=MAX_FRAMES
ani_tc1 = animation.FuncAnimation(f_tc1, animate_tc, frames=100, fargs=(a_tc1, y_tc1_List, b'tc1', ser), interval=1000) #, save_count=MAX_FRAMES
app.mainloop()
ser.close()


