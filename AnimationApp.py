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
        self._name_of_file = None
        self._number_of_measurements = None
        self._delay_between_measurements = None # in seconds

        # Experiment results
        self._some_result = 10 # S: just to mark that here will be some calculated values

        self.animation_need_init_function_flag = True
        self.data_file = None
        self.writer = None

        self.start_time = float(0.0)
        
        self.animation_function = animation.FuncAnimation(fig, self.animation_loop, frames=100, fargs=(axs, controller), interval=10)
        self.doAnimation_flag = False

    def animation_setup(self):
        # TODO: put it into animation_init_function()
        self.animation_need_init_function_flag = False
        name_of_file = self._name_of_file + ".csv"
        # 
        # Opening/Creating a file and creating writer
        # S: as I understand, default newline='\n'
        self.data_file = open(file=name_of_file, mode='w', newline='')
        # S: csv.writer(file=, delimeter=, dialect='excel-tab') 
        #    I dont understad on practice what the 'dialect' argument adding changes...
        self.writer = csv.writer(self.data_file, delimiter=',')

         # Creating the header row list for data table:
        dataHeader = []
        dataHeader.append("Sample")
        dataHeader.append("Time")
        
        for channel in (0, 1, 2):
            dataHeader.append("Channel" + str(channel))
            
        # Writeing dataHeader to file
        self.writer.writerow(dataHeader)
        # Printing dataHeader to console
        for head in dataHeader:
            print(f'{head:12}', end='')
        print()
        self.start_time = time.perf_counter()

    def animation_loop(self, i, axs, controller): 
        try:
            if (self.x_list[-1] >= self._number_of_measurements):
                self.finish()
        except:
            pass
        
        if (self.doAnimation_flag == True):
            if (self.animation_need_init_function_flag == True):
                self.animation_setup()
            
            # Calculating a measurement time from the begine of the experiment
            sample_time = time.perf_counter()
            sample_time_from_start = sample_time - self.start_time

            # Adding the number of measurements to x_list
            number_of_measurement = None
            try:
                number_of_measurement = self.x_list[-1] + 1
            except:
                number_of_measurement = 0
            finally:
                self.x_list.append(number_of_measurement)
            

            # Read a single value from each selected channel
            new_tc0_value = self.data_reader.read_tc0()
            new_tc1_value = self.data_reader.read_tc1()
            new_tc2_value = self.data_reader.read_tc2()

            # Creating a list of the new measurements data
            dataRow = []
            dataRow.append(number_of_measurement)
            dataRow.append(sample_time_from_start)
            dataRow.append(new_tc0_value)
            dataRow.append(new_tc1_value)
            dataRow.append(new_tc2_value)
            self.writer.writerow(dataRow)

            # Printing dataRow to console
            print('\r{:6}'.format(number_of_measurement), end='')
            print('{:10.2f} s '.format(sample_time_from_start), end='')
            print('{:10.2f} C'.format(new_tc0_value), end='')
            print('{:10.2f} C'.format(new_tc1_value), end='')
            print('{:10.2f} C'.format(new_tc2_value), end='', flush=True)

            # Adding new data to the y_lists of the axes
            self.tc0_list.append(new_tc0_value)
            self.tc1_list.append(new_tc1_value)
            self.tc2_list.append(new_tc2_value)

            # Slicing last parts of axes data listss
            self.x_list = self.x_list[-10:]
            self.tc0_list = self.tc0_list[-10:]
            self.tc1_list = self.tc1_list[-10:]
            self.tc2_list = self.tc2_list[-10:]

            # Updating axes
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

        # print("Animation_flag is: " + str(self.doAnimation_flag))

    def start(self, 
            #   Sample settings
              sample_height,
            #   Experiental settings
              name_of_file, number_of_measurements, delay_between_measurements):
        # Sample height
        try:
            self._sample_height = float(sample_height)
        except:
            self._sample_height = 10
            print("MyExeption: AnimationApp.py <Convertation sample_height to float is failed>")
        
        # Name of file
        self._name_of_file = name_of_file

        # Quantity of measurements
        try:
            self._number_of_measurements = int(number_of_measurements)
        except:
            self._number_of_measurements = 10
            print("MyExeption: AnimationApp.py <Convertation number_of_measurement to int is failed>")
        
        # Delay between measurements
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