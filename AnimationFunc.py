

def animate(i, axs, controller): 
    if (controller.doAnimation == True):
        new_tc0_value = controller.data_reader.read_tc0()
        new_tc1_value = controller.data_reader.read_tc1()
        new_tc2_value = controller.data_reader.read_tc2()
        
        try:
            number_of_measurement = controller.x_list[-1] + 1
        except:
            number_of_measurement = 0
        finally:
            controller.x_list.append(number_of_measurement)

        controller.tc0_list.append(new_tc0_value)
        controller.tc1_list.append(new_tc1_value)
        controller.tc2_list.append(new_tc2_value)

        controller.x_list = controller.x_list[-10:]

        controller.tc0_list = controller.tc0_list[-10:]
        controller.tc1_list = controller.tc1_list[-10:]
        controller.tc2_list = controller.tc2_list[-10:]

        axs[0].clear()
        axs[0].plot(controller.x_list,controller.tc0_list)
        axs[0].set_ylim(15, 45)
        axs[0].set_title("Thermocouple " + str(0))
        axs[0].set_ylabel("Temperature, deg C")

        axs[1].clear()
        axs[1].plot(controller.x_list,controller.tc1_list)
        axs[1].set_ylim(15, 45)
        axs[1].set_title("Thermocouple " + str(1))
        axs[2].set_ylabel("Temperature, deg C")

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
        print("Animation is: " + str(controller.doAnimation))