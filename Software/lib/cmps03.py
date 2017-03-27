import smbus


class CMPS03():

	CMPS03_SOFTVER = 0
	CMPS03_BEARING = 1
	CMPS03_DEGBEAR = 2
	CMPS03_DEGBEAR1 = 3

	CMPS03_UNLOCK1 = 12
	CMPS03_UNLOCK2 = 13
	CMPS03_UNLOCK3 = 14
	CMPS03_REGADDR = 15
	
	def __init__(self, address=0x60, bus_num=1):
		self.bus_num = bus_num
		self.address = address
		self.bus = smbus.SMBus(bus=bus_num)

	def read_reg(self, reg_addr):
		try:
			return self.bus.read_byte_data(self.address, reg_addr)
		except IOError:
			print "Error Reading CMPS03"
			return 0

	def write_reg(self, reg_addr, value):
		try:
			self.bus.write_byte_data(self.address, reg_addr, value)
		except IOError:
			print "Error Writing CMPS03"

	def softwareVersion(self):
		return self.read_reg(self.CMPS03_SOFTVER)

	def bearing255(self):
		bear = self.read_reg(self.CMPS03_BEARING)
		return bear #Compass Bearing as a byte, i.e. 0-255 for a full circle

	def bearing3599(self):  
		bear1 = self.read_reg(self.CMPS03_DEGBEAR)
		bear2 = self.read_reg(self.CMPS03_DEGBEAR1)
		bear = (bear1 << 8) + bear2
		bear = bear/10.0
		return bear #Compass Bearing as a word, i.e. 0-3599 for a full circle, representing 0-359.9 degrees.

	def calibrate(self):

		raw_input("Initial Position")
		self.write_reg(self.CMPS03_REGADDR, 0xFF)

		raw_input("Turn 90 degrees Right")
		self.write_reg(self.CMPS03_REGADDR, 0xFF)

		raw_input("Turn 90 degrees Right")
		self.write_reg(self.CMPS03_REGADDR, 0xFF)

		raw_input("Turn 90 degrees Right")
		self.write_reg(self.CMPS03_REGADDR, 0xFF)

		print "Sucessfully Calibrated!"

	def changeScanTime(self, mode):
		"""
		Mode |  Scan Period
		0		300mS
		1		100mS
		2		33mS
		"""
		scanPeriods = [0x10, 0x11, 0x12]

		self.write_reg(self.CMPS03_UNLOCK1, 0x55)
		self.write_reg(self.CMPS03_UNLOCK2, 0x5A)
		self.write_reg(self.CMPS03_UNLOCK3, 0xA5)
		self.write_reg(self.CMPS03_REGADDR, scanPeriods[mode])

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

		self.write_reg(self.CMPS03_UNLOCK1, 0xA0)
		self.write_reg(self.CMPS03_UNLOCK2, 0xAA)
		self.write_reg(self.CMPS03_UNLOCK3, 0xA5)
		self.write_reg(self.CMPS03_REGADDR, adresses[newAddr])

	def factoryReset(self):
		self.write_reg(self.CMPS03_UNLOCK1, 0x55)
		self.write_reg(self.CMPS03_UNLOCK2, 0x5A)
		self.write_reg(self.CMPS03_UNLOCK3, 0xA5)
		self.write_reg(self.CMPS03_REGADDR, 0xF2)