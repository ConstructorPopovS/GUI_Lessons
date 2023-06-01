import matplotlib.animation as animation
import DataReader
import csv #for saving data in csv format file
import time #for saving time of each measurement

class AnimationApp():

    def __init__(self, fig, axs, controller):

        self.data_reader = DataReader.DataReader()

        self.x_list = []
        self.tc0_list = []
        self.tc1_list = []
        self.tc2_list = []

        self.animation_need_init_function_flag = True
        self.data_file = None
        self.writer = None
        self.name_of_file = "new_data_file"

        self.start_time = float(0.0)
        
        self.animation_function = animation.FuncAnimation(fig, self.animate, frames=100, fargs=(axs, controller), interval=1000)
        self.doAnimation_flag = False

    def animate(self, i, axs, controller): 
        if (self.doAnimation_flag == True):
            # TODO: put it into animation_init_function()
            if (self.animation_need_init_function_flag == True):
                self.animation_need_init_function_flag = False

                self.data_file = open("Some_File.txt", 'w')
                self.writer = csv.writer(self.data_file)
                print("File is created")

                channels = (0, 1, 2)

                # Display the header row for data table:
                dataHeader = "    Sample,    "
                dataHeader += "  Time,    "
                for channel in channels:
                    dataHeader += " Channel" + str(channel) + ","
                
                self.start_time = time.perf_counter()

                print(dataHeader)
                self.data_file.write(dataHeader + '\n')

            number_of_measurement = None
            try:
                number_of_measurement = self.x_list[-1] + 1
            except:
                number_of_measurement = 0
            finally:
                self.x_list.append(number_of_measurement)
            
            dataRow = []
            dataRow.append(number_of_measurement)

            # Display the updated number of measurement count
            print('\r{:6d}'.format(number_of_measurement), end='')

            sample_time = time.perf_counter()
            sample_time_from_start = sample_time - self.start_time
            dataRow.append(sample_time_from_start)
            print('{:12.2f} s'.format(sample_time_from_start), end='')

            # Read a single value from each selected channel
            new_tc0_value = self.data_reader.read_tc0()
            dataRow.append(new_tc0_value)
            print('{:12.2f} C'.format(new_tc0_value), end='')

            new_tc1_value = self.data_reader.read_tc1()
            dataRow.append(new_tc1_value)
            print('{:12.2f} C'.format(new_tc1_value), end='')

            new_tc2_value = self.data_reader.read_tc2()
            dataRow.append(new_tc2_value)
            print('{:12.2f} C'.format(new_tc2_value), end='', flush=True)

            self.tc0_list.append(new_tc0_value)
            self.tc1_list.append(new_tc1_value)
            self.tc2_list.append(new_tc2_value)

            self.writer.writerow(dataRow)
    
            self.x_list = self.x_list[-10:]
    
            self.tc0_list = self.tc0_list[-10:]
            self.tc1_list = self.tc1_list[-10:]
            self.tc2_list = self.tc2_list[-10:]
    
            axs[0].clear()
            axs[0].plot(self.x_list,self.tc0_list)
            axs[0].set_ylim(15, 45)
            axs[0].set_title("Thermocouple " + str(0))
            axs[0].set_ylabel("T, deg C")
    
            axs[1].clear()
            axs[1].plot(self.x_list,self.tc1_list)
            axs[1].set_ylim(15, 45)
            axs[1].set_title("Thermocouple " + str(1))
            axs[1].set_ylabel("T, deg C")
    
            axs[2].clear()
            axs[2].plot(self.x_list,self.tc2_list)
            axs[2].set_ylim(15, 45)
            axs[2].set_title("Thermocouple " + str(2))
            axs[2].set_ylabel("T, deg C")
    
            # try:
            #     axs.set_xlim(controller.x_list[-10], (controller.x_list[-0]))
            # except:
            #     axs.set_xlim(0, 10)
    
            # 
        # print("Animation_flag is: " + str(self.doAnimation_flag))

    def start(self):
        print("Start")
        self.doAnimation_flag = True
        self.animation_need_init_function_flag = True
        try:
            self.animation_function.resume()
        except:
            pass


    def finish(self):
        self.doAnimation_flag = False
        try:
            self.data_file.close()
            self.animation_function.pause()
        except:
            pass
        self.animation_need_init_function_flag = True

    def pause(self):
        self.doAnimation_flag = False
        try:
            self.animation_function.pause()
        except:
            pass

    def resume(self):
        self.doAnimation_flag = True
        try:
            self.animation_function.resume()
        except:
            pass

    def get_name_of_file(self):
        return self.name_of_file