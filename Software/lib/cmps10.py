import smbus
import time

class CMPS10():
	CMPS10_SOFTVER = 0

	CMPS10_BEARING = 1
	CMPS10_DEGBEAR = 2
	CMPS10_DEGBEAR1 = 3
	CMPS10_PICH = 4
	CMPS10_ROLL = 5
	
	CMPS10_REGADDR = 22
	
	def __init__(self, address=0x60, bus_num=1):
		self.bus_num = bus_num
		self.address = address
		self.bus = smbus.SMBus(bus=bus_num)

	def read_reg(self, reg_addr):
		try:
			return self.bus.read_byte_data(self.address, reg_addr)
		except IOError:
			print "Error Reading CMPS10"
			return 0

	def write_reg(self, reg_addr, value):
		try:
			self.bus.write_byte_data(self.address, reg_addr, value)
			time.sleep(0.1)
		except IOError:
			print "Error Writing CMPS10"

	def softwareVersion(self):
		return self.read_reg(self.CMPS10_SOFTVER)

	def bearing255(self):
		bear = self.read_reg(self.CMPS10_BEARING)
		return bear #Compass Bearing as a byte, i.e. 0-255 for a full circle

	def bearing3599(self):  
		bear1 = self.read_reg(self.CMPS10_DEGBEAR)
		bear2 = self.read_reg(self.CMPS10_DEGBEAR1)
		bear = (bear1 << 8) + bear2
		bear = bear/10.0
		return bear #Compass Bearing as a word, i.e. 0-3599 for a full circle, representing 0-359.9 degrees.

	def pich(self):
		pich = self.read_reg(self.CMPS10_PICH)
		return pich
	
	def roll(self):
		roll = self.read_reg(self.CMPS10_ROLL)
		return roll

	def calibrate(self):
		self.write_reg(self.CMPS10_REGADDR, 0xF0)

		raw_input("Initial Position")
		self.write_reg(self.CMPS10_REGADDR, 0xF5)

		#Led Turn On If Calibration Mode Started Sucessfully

		raw_input("Turn 90 degrees Right")
		self.write_reg(self.CMPS10_REGADDR, 0xF5)

		raw_input("Turn 90 degrees Right")
		self.write_reg(self.CMPS10_REGADDR, 0xF5)

		raw_input("Turn 90 degrees Right")
		self.write_reg(self.CMPS10_REGADDR, 0xF5)

		print "Sucessfully Calibrated!"


	def changeAdress(self, newAddr):
		"""
		ID | Adress
		0	 0xC0
		1	 0xC2
		2	 0xC4
		3	 0xC6
		4	 0xC8
		5	 0xCA
		6	 0xCC
		7	 0xCE
		"""

		adresses = [0xC0, 0xC2, 0xC4, 0xC6, 0xC8, 0xCA, 0xCC, 0xCE]

		self.write_reg(self.CMPS10_REGADDR, 0xA0)
		self.write_reg(self.CMPS10_REGADDR, 0xAA)
		self.write_reg(self.CMPS10_REGADDR, 0xA5)
		self.write_reg(self.CMPS10_REGADDR, adresses[newAddr])

	def factoryReset(self):
		self.write_reg(self.CMPS10_REGADDR, 0x20)
		self.write_reg(self.CMPS10_REGADDR, 0x2A)
		self.write_reg(self.CMPS10_REGADDR, 0x60)