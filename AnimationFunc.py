

def animate(i, axs, controller): 
    if (controller.doAnimation == True):
        new_tc0_value = controller.data_reader.read_tc0()
        new_tc1_value = controller.data_reader.read_tc1()
        new_tc2_value = controller.data_reader.read_tc2()
        print()

        controller.x_list.append(i)
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
        # print("x_list: " + str(controller.x_list))
        # print("y_list: " + str(controller.tc0_list))

        axs[1].clear()
        axs[1].plot(controller.x_list,controller.tc1_list)
        axs[1].set_ylim(15, 45)

        axs[2].clear()
        axs[2].plot(controller.x_list,controller.tc2_list)
        axs[2].set_ylim(15, 45)

        # try:
        #     axs.set_xlim(controller.x_list[-10], (controller.x_list[-0]))
        # except:
        #     axs.set_xlim(0, 10)

        # axs.set_title("Thermocouple " + tcData.name.decode())
        # axs.set_ylabel("Temperature, deg C")
    else:
        print("Animation is: " + str(controller.doAnimation))