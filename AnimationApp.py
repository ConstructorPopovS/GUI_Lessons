import matplotlib.animation as animation
import DataReader

class AnimationApp():

    def __init__(self, fig, axs, controller):
        self.animation_function = animation.FuncAnimation(fig, self.animate, frames=100, fargs=(axs, self), interval=1000)
        self.doAnimation_flag = False
        self.data_reader = DataReader.DataReader()
        self.x_list = []
        self.tc0_list = []
        self.tc1_list = []
        self.tc2_list = []

    def animate(self, i, axs, controller): 
        if (self.doAnimation_flag == True):
            print("Animation!")
            new_tc0_value = self.data_reader.read_tc0()
            new_tc1_value = self.data_reader.read_tc1()
            new_tc2_value = self.data_reader.read_tc2()
            
            try:
                number_of_measurement = self.x_list[-1] + 1
            except:
                number_of_measurement = 0
            finally:
                controller.x_list.append(number_of_measurement)
    
            self.tc0_list.append(new_tc0_value)
            self.tc1_list.append(new_tc1_value)
            self.tc2_list.append(new_tc2_value)
    
            self.x_list = controller.x_list[-10:]
    
            self.tc0_list = controller.tc0_list[-10:]
            self.tc1_list = controller.tc1_list[-10:]
            self.tc2_list = controller.tc2_list[-10:]
    
            axs[0].clear()
            axs[0].plot(controller.x_list,controller.tc0_list)
            axs[0].set_ylim(15, 45)
            axs[0].set_title("Thermocouple " + str(0))
            axs[0].set_ylabel("Temperature, deg C")
    
            axs[1].clear()
            axs[1].plot(controller.x_list,controller.tc1_list)
            axs[1].set_ylim(15, 45)
            axs[1].set_title("Thermocouple " + str(1))
            axs[1].set_ylabel("Temperature, deg C")
    
            axs[2].clear()
            axs[2].plot(controller.x_list,controller.tc2_list)
            axs[2].set_ylim(15, 45)
            axs[2].set_title("Thermocouple " + str(2))
            axs[2].set_ylabel("Temperature, deg C")
    
            # try:
            #     axs.set_xlim(controller.x_list[-10], (controller.x_list[-0]))
            # except:
            #     axs.set_xlim(0, 10)
    
            # 
        else:
            print("Animation is: " + str(self.doAnimation_flag))

    def resumeAnimation(self):
        self.doAnimation_flag = True
        try:
            pass
            self.animation_function.resume()
        except:
            pass

    def stopAnimation(self):
        self.doAnimation_flag = False
        try:
            self.animation_function.pause()
            print("Stop")
        except:
            pass