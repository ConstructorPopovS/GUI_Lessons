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

ser = serial.Serial(port='/dev/ttyACM0',baudrate=9600,timeout=15)

class ThermcouplePlotData():
    def __init__(self, name): #tcData.name should be in byte format: b'name'
        self.x_List = []
        self.y_List = []
        self.name = name

def animate(i, axs, tcData, ser): 
    # tcData.name should be in byte format: (a_tc, y_tc_List, b'command_to_send', ser)
    ser.write(tcData.name)
    aData_str = ser.readline().decode('ascii')
    # aData_str = str(random.randrange(20,40))

    try:
        aData_float = float(aData_str)
        tcData.y_List.append(aData_float)
        print(tcData.name.decode() + " = "+ str(aData_float))
    except:
        print("UserExeption: convertation tc_str to float is failed")
        tcData.y_List.append(25)

    try:
        pass
    except:
        print("UserExeption: x.append")

    tcData.x_List.append(i)

    tcData.y_List = tcData.y_List[-10:]
    tcData.x_List = tcData.x_List[-10:]

    axs.clear()
    axs.plot(tcData.x_List,tcData.y_List) #xList,
    axs.set_ylim(15, 45)

    try:
        axs.set_xlim(tcData.x_List[-10], (tcData.x_List[-10] + 10))
    except:
        axs.set_xlim(0, 10)

    axs.set_title("Thermocouple " + tcData.name.decode())
    axs.set_ylabel("Temperature, deg C")

def full_animation(i, axs, controller, ser):
    if(controller.doAnimation == True):
        animate(i, axs[0], controller.tcData0, ser)
        animate(i, axs[1], controller.tcData1, ser)
        animate(i, axs[2], controller.tcData2, ser)
        print("============================")
    else:
        print("Value controller.doAnimation = " + str(controller.doAnimation))

def confirm(root):
    answer = askyesno(title='Exit', message='Do You Want To Exit?')
    if answer:
        ser.close()
        print("Serial is closed from confirm()")
        root.destroy()

def startAnimation(controller):
    print("Was: " + str(controller.doAnimation))
    controller.doAnimation = True
    print("Setted: " +str(controller.doAnimation))

def stopAnimation(controller):
    print("Was: " + str(controller.doAnimation))
    controller.doAnimation = False
    print("Setted: " +str(controller.doAnimation))

class MyApp(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        # tk.Tk.iconbitmap(self)
        tk.Tk.wm_title(self, "Thermal Conductivity Measurement Program")

        self.tcData0 = ThermcouplePlotData(b'tc0')
        self.tcData1 = ThermcouplePlotData(b'tc1')
        self.tcData2 = ThermcouplePlotData(b'tc2')

        self.doAnimation = False

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
# ani_0 = animation.FuncAnimation(fig, animate, frames=100, fargs=(axs[0], x_List, y0_List, ser, b'tc0'), interval=1000) #, save_count=MAX_FRAMES

ani = animation.FuncAnimation(fig, full_animation, frames=100, fargs=(axs, app, ser), interval=1000) #, save_count=MAX_FRAMES

# ani = animation.FuncAnimation(fig, animate_all_plots, frames=100, fargs=(ser, x_List,
#                                                                          axs[0], y0_List, b'tc0',
#                                                                          axs[1], y1_List, b'tc1',
#                                                                          axs[2], y2_List, b'tc2',), interval=1000)
app.mainloop()
ser.close()
print("Serial is closed")


