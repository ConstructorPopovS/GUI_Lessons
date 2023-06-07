import matplotlib.animation as animation
import csv #for saving data in csv format file
import time #for saving time of each measurement
import DataReader

class AnimationApp():

    def __init__(self, fig, axs, controller):

        self.data_reader = DataReader.DataReader()

        # Lists of data
        self.numbers_of_measurings_list = []
        self.time_list = []
        self.tc0_list = []
        self.tc1_list = []
        self.tc2_list = []
        self.tc3_list = []

        # Sample settings
        self._sample_height = 9.8 # in mm

        # Experiment settings
        self._name_of_file = None
        self._number_of_measurements = None
        self._delay_between_measurements = None # in seconds

        # Experiment results
        self._some_result = 10 # S: just to mark that here will be some calculated values

        self.data_file = None
        self.writer = None

        self.start_time = float(0.0)
        
        self.doAnimation_flag = False
        self.animation_function = animation.FuncAnimation(fig, self.animation_loop, frames=100, fargs=(axs, controller), interval=100)

    def animation_setup(self):
        # self.animation_need_init_function_flag = False
        name_of_file = self._name_of_file + ".csv"

        # Opening/Creating a file and creating writer
        # S: as I understand, default newline='\n'
        self.data_file = open(file=name_of_file, mode='w', newline='')
        # S: csv.writer(file=, delimeter=, dialect='excel-tab') 
        #    I dont understad on practice what the 'dialect' argument adding changes...
        self.writer = csv.writer(self.data_file, delimiter=',')

         # Create the header row list for data table:
        dataHeader = []
        dataHeader.append("Sample")
        dataHeader.append("Time")
        
        for channel in (0, 1, 2, 3):
            dataHeader.append("Channel" + str(channel))
            
        # Write dataHeader to file
        self.writer.writerow(dataHeader)
        # Print name of the experiment to console
        print(f'|||||||| Experiment: {self._name_of_file} ||||||||')
        # Print dataHeader to console
        for head in dataHeader:
            print(f'{head:12}', end='')
        print()
        self.start_time = time.perf_counter()

    def animation_loop(self, i, axs, controller): 
        # S: to pause/resume animation we can use animation.pause() and animation.resume()
        #    but when the GUIApp is run firstly, for some reason those functions are not working
        #    so I created this doAnimation_flag and setted default value as False 
        #    to "pause" animation at the start of GUIApp
        if (self.doAnimation_flag == True):
            # Check 0: "Last number of measurements (quantity)"
            try:
                if (self.numbers_of_measurings_list[-1] >= self._number_of_measurements):
                    self.finish(controller=controller)
                    return
            except:
                pass
            # Check 1: "Is it a first measure?"
            try:
                self.numbers_of_measurings_list[-1]

                # Check 2: "Time between measurements"
                try:
                    time_now = time.perf_counter()
                    time_now_from_start = time_now - self.start_time
                    time_now_from_the_last_measurement = time_now_from_start - self.time_list[-1]

                    if (time_now_from_the_last_measurement < self._delay_between_measurements):
                        return
                except:
                    pass
            except:
                pass
                # self.animation_setup()
            
            # |||||||||GETTING/CALCULATING A NEW DATA POINT VALUES|||||||||||||||
            # Number of measuring
            number_of_a_new_measurement = None
            try:
                number_of_a_new_measurement = self.numbers_of_measurings_list[-1] + 1
            except:
                number_of_a_new_measurement = 0
            finally:
                self.numbers_of_measurings_list.append(number_of_a_new_measurement)

            # Data from each thermocouples
            new_tc0_value = self.data_reader.read_tc0()
            new_tc1_value = self.data_reader.read_tc1()
            new_tc2_value = self.data_reader.read_tc2()
            new_tc3_value = self.data_reader.read_tc3()

            # Time from start
            measurement_time = time.perf_counter()
            new_measurement_time_from_start = measurement_time - self.start_time

            # Adding new data to all data lists
            self.time_list.append(new_measurement_time_from_start)
            self.tc0_list.append(new_tc0_value)
            self.tc1_list.append(new_tc1_value)
            self.tc2_list.append(new_tc2_value)            
            self.tc3_list.append(new_tc3_value)         
            # |||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||

            # Creating a list of the new measurements data to save in the file
            dataRow = []
            dataRow.append(number_of_a_new_measurement)
            dataRow.append(new_measurement_time_from_start)
            dataRow.append(new_tc0_value)
            dataRow.append(new_tc1_value)
            dataRow.append(new_tc2_value)
            dataRow.append(new_tc3_value)
            self.writer.writerow(dataRow)


            # CONSOLE INTERFACE
            print('\r{:6}'.format(number_of_a_new_measurement), end='')
            print('{:10.2f} s '.format(new_measurement_time_from_start), end='')
            print('{:10.2f} C'.format(new_tc0_value), end='')
            print('{:10.2f} C'.format(new_tc1_value), end='')
            print('{:10.2f} C'.format(new_tc2_value), end='')
            print('{:10.2f} C'.format(new_tc3_value), end='', flush=True)

            # Slicing the last parts of the axes data lists
            self.numbers_of_measurings_list = self.numbers_of_measurings_list[-10:]
            self.tc0_list = self.tc0_list[-10:]
            self.tc1_list = self.tc1_list[-10:]
            self.tc2_list = self.tc2_list[-10:]
            self.tc3_list = self.tc2_list[-10:]

            # Updating axes
            self.update_axes(axs=axs)

            # Updating "out" lables
            controller.frames["MainPageGUI"].label_number_of_measurement.config(
                text = "Measurement number: " + str(number_of_a_new_measurement))
            controller.frames["MainPageGUI"].label_tc0.config(text = "tc0: " + str(new_tc0_value))
            controller.frames["MainPageGUI"].label_tc1.config(text = "tc1: " + str(new_tc1_value))
            controller.frames["MainPageGUI"].label_tc2.config(text = "tc2: " + str(new_tc2_value))
            controller.frames["MainPageGUI"].label_tc3.config(text = "tc3: " + str(new_tc3_value))

        # print("Animation_flag is: " + str(self.doAnimation_flag))
    
    def update_axes(self, axs):
            axs[0].clear()
            axs[0].plot(self.numbers_of_measurings_list,self.tc0_list)
            axs[0].set_ylim(15, 45)
            axs[0].set_title("Thermocouple " + str(0))
            axs[0].set_ylabel("T, deg C")
    
            axs[1].clear()
            axs[1].plot(self.numbers_of_measurings_list,self.tc1_list)
            axs[1].set_ylim(15, 45)
            axs[1].set_title("Thermocouple " + str(1))
            axs[1].set_ylabel("T, deg C")
    
            axs[2].clear()
            axs[2].plot(self.numbers_of_measurings_list,self.tc2_list)
            axs[2].set_ylim(15, 45)
            axs[2].set_title("Thermocouple " + str(2))
            axs[2].set_ylabel("T, deg C")

            axs[3].clear()
            axs[3].plot(self.numbers_of_measurings_list,self.tc2_list)
            axs[3].set_ylim(15, 45)
            axs[3].set_title("Thermocouple " + str(3))
            axs[3].set_ylabel("T, deg C")
    
    def start(self, axs,
            #   Sample settings
              sample_height,
            #   Experiental settings
              name_of_file, number_of_measurements, delay_between_measurements):
        
        # Updating axes
        self.update_axes(axs=axs)
    
        # Sample height
        try:
            self._sample_height = float(sample_height)
        except:
            self._sample_height = 10
            print("MyException from AApp.start(): Convertation sample_height to float is failed")
        
        # Name of file
        self._name_of_file = name_of_file

        # Quantity of measurements
        try:
            self._number_of_measurements = int(number_of_measurements)
        except:
            self._number_of_measurements = 10
            print("MyException from AApp.start(): Convertation number_of_measurement to int is failed")
        
        # Delay between measurements
        try:
            self._delay_between_measurements = float(delay_between_measurements)
        except:
            self._delay_between_measurements = 0.5
            print("MyException from AApp.start(): Convertation delay_between_measurement to float is failed")

        self.animation_setup()
        self.doAnimation_flag = True
        # self.animation_need_init_function_flag = True
        try:
            self.animation_function.resume()
        except:
            print("MyException from AApp.start(): animation.resume()")


    def finish(self, controller):
        self.doAnimation_flag = False
        print('\n\n', end='')

        try:
            try:
                self.animation_function.pause()
            except:
                print("MyException from AApp.finish(): animation.pause()")
            self.data_file.close()
            self.numbers_of_measurings_list = []
            self.tc0_list = []
            self.tc1_list = []
            self.tc2_list = []
            self.tc3_list = []
            self.data_file = None
            self.writer = None
        except:
            print("MyException from AApp.finish()")

        controller.frames["MainPageGUI"].button_start_animation['state']="normal"
        controller.frames["MainPageGUI"].button_pause_animation['state']="disabled"
        controller.frames["MainPageGUI"].button_resume_animation['state']="disabled"
        controller.frames["MainPageGUI"].button_finish_animation['state']="disabled"

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