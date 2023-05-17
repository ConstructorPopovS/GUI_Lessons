import serial

class DataReader():
    def __init__(self) -> None:
        self.ser = serial.Serial(port='/dev/ttyACM0',baudrate=9600,timeout=15)
        self.NameTC = [b'tc0', b'tc1', b'tc2']
        

    def __read(self, name):
        self.ser.write(name)
        aData_str = "0"
        aData_str = self.ser.readline().decode('ascii')
        # aData_str = str(random.randrange(20,40))

        try:
            aData_float = float(aData_str)
            print(name.decode() + " = "+ str(aData_float), end='\t')
            return aData_float
        except:
            print("UserExeption: convertation tc_str to float is failed")
            return 0
    
    def read_tc0(self):
        value = self.__read(self.NameTC[0])
        return value
    
    def read_tc1(self):
        value = self.__read(self.NameTC[1])
        return value
    
    def read_tc2(self):
        value = self.__read(self.NameTC[2])
        return value
