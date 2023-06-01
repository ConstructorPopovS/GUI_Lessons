import matplotlib.animation as animation
import csv #for saving data in csv format file
import time #for saving time of each measurement
import DataReader

class AnimationApp():

    def __init__(self, fig, axs, controller):

        self.data_reader = DataReader.DataReader()

        # Lists for plot axes
        self.x_list = []
        self.tc0_list = []
        self.tc1_list = []
        self.tc2_list = []

        # Sample settings
        self._sample_height = 9.8 # in mm

        # Experiment settings
        self._name_of_file = "new_data_file"
        self._number_of_measurements = 120
        self._delay_between_measurements = 0.9 # in seconds

        # Experiment results
        self._some_result = 10 # S: just to mark that here will be some calculated values

        self.animation_need_init_function_flag = True
        self.data_file = None
        self.writer = None

        self.start_time = float(0.0)
        
        self.animation_function = animation.FuncAnimation(fig, self.animate, frames=100, fargs=(axs, controller), interval=1000)
        self.doAnimation_flag = False

    def animate(self, i, axs, controller): 
        if (self.doAnimation_flag == True):
            # TODO: put it into animation_init_function()
            if (self.animation_need_init_function_flag == True):
                self.animation_need_init_function_flag = False

                name_of_file = self._name_of_file + ".txt"
                self.data_file = open(name_of_file, 'w')
                self.writer = csv.writer(self.data_file)
                print("File is created")

                channels = (0, 1, 2)

                # Display the header row for data table:
                dataHeader = []
                dataHeader.append("Sample")
                dataHeader.append("Time")
                for channel in channels:
                    dataHeader.append("Channel" + str(channel))
                
                # print(dataHeader)
                # self.data_file.write(dataHeader + '\n')
                self.writer.writerow(dataHeader)
                for head in dataHeader:
                    print(f'{head:20}', end='')
                print()

                self.start_time = time.perf_counter()

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
            print('\r{:6}'.format(number_of_measurement), end='')

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

    def start(self, 
            #   Sample settings
              sample_height,
            #   Experiental settings
              name_of_file, number_of_measurements, delay_between_measurements):
        print("Start")
        try:
            self._sample_height = float(sample_height)
        except:
            self._sample_height = 10
            print("MyExeption: AnimationApp.py <Convertation sample_height to float is failed>")

        self._name_of_file = name_of_file
        try:
            self._number_of_measurements = int(number_of_measurements)
        except:
            self._number_of_measurements = 10
            print("MyExeption: AnimationApp.py <Convertation number_of_measurement to int is failed>")
        try:
            self._delay_between_measurements = float(delay_between_measurements)
        except:
            self._delay_between_measurements = 0.5
            print("MyExeption: AnimationApp.py <Convertation delay_between_measurement to float is failed>")
        
        print('h:{0} name:{1} number:{2} delay:{3}'.format(self._sample_height,
                                                   self._name_of_file,
                                                   self._number_of_measurements,
                                                   self._delay_between_measurements))


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

    def get_sample_height(self):
        return self._sample_height
    
    def get_name_of_file(self):
        return self._name_of_file
    
    def get_number_of_measurements(self):
        return self._number_of_measurements
    
    def get_delay_between_measurements(self):
        return self._delay_between_measurements