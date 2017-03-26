import smbus
import time

class CMPS03():
	
	def __init__(self, address=0x60, bus_num=1):
		self.bus_num = bus_num
		self.address = address
		self.bus = smbus.SMBus(bus=bus_num)
	
	def bearing255(self):
		bear = self.bus.read_byte_data(self.address, 1)
		return bear #Compass Bearing as a byte, i.e. 0-255 for a full circle

	def bearing3599(self):  
		bear1 = self.bus.read_byte_data(self.address, 2)

		time.sleep(0.00001)

		bear2 = self.bus.read_byte_data(self.address, 3)
		bear = (bear1 << 8) + bear2
		bear = bear/10.0
		return bear #Compass Bearing as a word, i.e. 0-3599 for a full circle, representing 0-359.9 degrees.

	def calibrate(self):

		raw_input("Initial Position")
		self.bus.write_byte_data(self.address, 255, 0xFF)

		#Pin 5 is High If Calibration Mode Started Sucessfully

		raw_input("Turn 90 degrees Right")
		self.bus.write_byte_data(self.address, 255, 0xFF)

		raw_input("Turn 90 degrees Right")
		self.bus.write_byte_data(self.address, 255, 0xFF)

		raw_input("Turn 90 degrees Right")
		self.bus.write_byte_data(self.address, 255, 0xFF)

		raw_input("Sucessfully Calibrated!")