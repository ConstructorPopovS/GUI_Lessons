# lesson from youtube "Live Maplotlib Graph in Tkinter Window in Python3 - Tkinter tutorial Python 3.4p.7"
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg #, NavigationToolbar2TkAgg
# S: I have made additional installations:
#  sudo apt-get install python3-pill.imagetk
#  sudo pip install ipython
from matplotlib.figure import Figure
import matplotlib.animation as animation
from matplotlib import style
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter.messagebox import askyesno 
import serial
import random

import AnimationFunc
import DataReader

LARGE_FONT = ("Verdana", 20)
style.use("ggplot")# ggplot, dark_background

# A figure with three subplots/axes
fig, axs = plt.subplots(3)
fig.set_figwidth(14)
fig.set_figheight(14)

axs[0].set_title("Thermocouple tc0")
# axs.set_ylabel("Temperature, deg C")

axs[1].set_title("Thermocouple tc1")
# axs.set_ylabel("Temperature, deg C")

axs[2].set_title("Thermocouple tc2")
# axs.set_ylabel("Temperature, deg C")

def confirm(root):
    answer = askyesno(title='Exit', message='Do You Want To Exit?')
    if answer:
        root.data_reader.close()
        print("Serial is closed from confirm()")
        root.destroy()

def startAnimation(controller):
    # controller.doAnimation = True
    controller.animation.resume()

def stopAnimation(controller):
    # controller.doAnimation = False
    controller.animation.pause()
    

class MyApp(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        # tk.Tk.iconbitmap(self)
        tk.Tk.wm_title(self, "Thermal Conductivity Measurement Program")

        self.data_reader = DataReader.DataReader()
        self.x_list = []
        self.tc0_list = []
        self.tc1_list = []
        self.tc2_list = []
        self.doAnimation = True

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

        self.animation = animation.FuncAnimation(fig, AnimationFunc.animate, frames=100, fargs=(axs, self), interval=1000)
        # print("Hm1")
        self.animation.pause()
        # print("Hm2")

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

        button1 = tk.Button(self, text="Back to Home", font = LARGE_FONT,
                            command=lambda: controller.show_frame(StartPage))
        button1.pack()

        # button2 = tk.Button(self, text="Visit page One", font = LARGE_FONT,
        #                     command=lambda: controller.show_frame(PageOne))
        button2 = tk.Button(self, text="Start Animation", font = LARGE_FONT,
                            command=lambda: startAnimation(controller))
        button2.pack()

        # button3 = tk.Button(self, text="Visit page Two", font = LARGE_FONT,
        #                     command=lambda: controller.show_frame(PageOne))
        button3 = tk.Button(self, text="Stop Animation", font = LARGE_FONT,
                            command=lambda: stopAnimation(controller))
        button3.pack()

        button4 = tk.Button(self, text="Print last value of tc0", font = LARGE_FONT,
                            command=lambda: print(controller.tcData0.y_List[-1]))
        button4.pack()
        
        canvas = FigureCanvasTkAgg(fig, self)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
 
        print("Page Three is initted")


app = MyApp()
MAX_FRAMES = 60
stopAnimation(app)

app.mainloop()
# ser.close()
print("Serial is closed")


