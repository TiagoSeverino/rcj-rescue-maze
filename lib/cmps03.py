import smbus

class CMPS03():

    #Modified From http://www.instructables.com/id/Raspberry-Pi-I2C-Python/step5/Example-1-CMPS03-Compass-Module/

    def __init__(self, address=0x60, bus_num=1):
        self.bus_num = bus_num
        self.address = address
        self.bus = smbus.SMBus(bus=bus_num)

    
    def bearing255(self):
            bear = self.bus.read_byte_data(address, 1)
            return bear #this returns the value to 1 decimal place in degrees. 

    def bearing3599(self):  
            bear1 = self.bus.read_byte_data(self.address, 2)
            bear2 = self.bus.read_byte_data(self.address, 3)
            bear = (bear1 << 8) + bear2
            bear = bear/10.0
            return bear #this returns the value as a byte between 0 and 255. 
