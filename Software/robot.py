import time
import RPi.GPIO as GPIO

from lib.l298n import L298N
from lib.srf04 import SRF04
from lib.cmps10 import CMPS10
# from lib.cmps03 import CMPS03
from lib.mlx90614 import MLX90614
from lib.lineSensor import LineSensor
from lib.kitDropper import KitDropper

class Robot():

	#Kit Dropper
	KitDropperPin = 7


	#MLX90614
	LeftThermometerAddr = 0x5a
	RightThermometerAddr = 0x2a

	#Line Sensor
	LineSensorPin = 36

	#SRF04
	LeftSonarTRIG = 8
	LeftSonarECHO = 11

	FrontSonarTRIG = 10
	FrontSonarECHO = 13

	RightSonarTRIG = 12
	RightSonarECHO = 15

	#Pin1, Pin2, PWM
	motorLeft = [35, 37, 33] #Motor in Left
	motorRight = [38, 40, 36] #Motor in Right

	#Vars

	#Arena Vars
	Lenght = 22.0
	Width = 13.0
	TileSize = 30.0

	#Localization Vars
	Direction = 0


	def __init__(self):

		GPIO.setwarnings(False)
		GPIO.setmode(GPIO.BOARD)

		#Line Sensor Setup
		self.LineSensor = LineSensor(self.LineSensorPin)

		#Kit Dropper Setup
		self.kitDropper = KitDropper(self.KitDropperPin)

		#Compass Setup
		self.compass = CMPS10()

		#Thermometer Setup
		self.thermometerLeft = MLX90614(self.LeftThermometerAddr)
		self.thermometerRight = MLX90614(self.RightThermometerAddr)

		#Sonar Setup
		self.sonar = []
		
		self.sonar.append(SRF04(self.LeftSonarTRIG, self.LeftSonarECHO))
		self.sonar.append(SRF04(self.FrontSonarTRIG, self.FrontSonarECHO)) 
		self.sonar.append(SRF04(self.RightSonarTRIG, self.RightSonarECHO))

		#Motors Setup
		self.MotorLeft = L298N(self.motorLeft[0], self.motorLeft[1], self.motorLeft[2])
		self.MotorRight = L298N(self.motorRight[0], self.motorRight[1], self.motorRight[2])


		#Register Position
		self.CompassOffset = self.compass.bearing3599()

	"""
	### Sensor Data ###
	"""


	def GetSonar(self, direction = "Front"):
		side = direction
		direction = direction.lower()

		sonar = 0
		
		if direction == "left":
			sonar = 0
		elif direction == "front":
			sonar = 1
		elif direction == "right":
			sonar = 2
		else:
			return 0

		distance = self.sonar[sonar].getCM()
		#print side, " Sonar: ", distance

		return distance

	def DropKit(self, ammount=1):
		self.Break()
		time.sleep(0.1)
		self.kitDropper.drop(ammount)


	def GetBearing(self):
		bearing = self.compass.bearing3599()

		bearing -= self.CompassOffset

		if bearing > 360.0:
			bearing -= 360.0
		elif bearing < 0.0:
			bearing += 360.0

		#print "Bearing: ", bearing

		return bearing


	def GetPich(self):
		pich = self.compass.pich()
		print "Pich: ", pich

		return pich


	def GetRoll(self):
		roll = self.compass.roll()
		print "Roll: ", roll

		return roll


	def GetTemperatureLeft(self):
		self.ambTempLeft = self.thermometerLeft.get_amb_temp()
		self.objTempLeft = self.thermometerLeft.get_obj_temp()

		print "Ambient Temperature Left: ", self.ambTempLeft
		print "Object Temperature Left: ", self.objTempLeft

		return (self.ambTempLeft, self.objTempLeft)


	def GetTemperatureRight(self):
		self.ambTempRight = self.thermometerRight.get_amb_temp()
		self.objTempRight = self.thermometerRight.get_obj_temp()

		print "Ambient Temperature Right: ", self.ambTempRight
		print "Object Temperature Right: ", self.objTempRight

		return (self.ambTempRight, self.objTempRight)

	"""
	### Precise Moving ###
	"""

	def GetTile(self, distance):
		tile = 0

		while distance >= 30.0:
			tile += 1
			distance -= 30.0

		return (tile, distance)

	def MoveTile(self):
		(tile, distance) = self.GetTile(self.GetSonar())

		if tile > 0:
			finalTile = tile - 1
		else:
			finalTile = 0

		while True:

			(tile, distance) = self.GetTile(self.GetSonar())

			if tile > finalTile:
				self.Forward()
			elif tile < finalTile:
				self.Backward()
			else:
				if distance < 6.5:
					self.Backward()
				elif distance > 9.5:
					self.Forward()
				else:
					self.Break()
					
					time.sleep(0.5)

					self.Rotate(self.Direction)

					print "Moved 1 Tile!"
					break


		else:
			print "Can't move Forward"



	def RotateLeft(self):

		if self.Direction == 1:
			self.Rotate(0)
		elif self.Direction == 2:
			self.Rotate(1)
		elif self.Direction == 3:
			self.Rotate(2)
		elif self.Direction == 0:
			self.Rotate(3)

		print "Rotated Left!"

	def RotateRight(self):
		
		if self.Direction == 1:
			self.Rotate(2)
		elif self.Direction == 2:
			self.Rotate(3)
		elif self.Direction == 3:
			self.Rotate(0)
		elif self.Direction == 0:
			self.Rotate(1)

		print "Rotated Right!"

	def Rotate(self, position, loop = True):
		while True:
			
			direction = self.GetBearing()
			rotateSpeed = 25

			if position == 0: ### Rotate To Direction 0
				if direction < 358 and direction >= 180.0:
					self.Right(speed = rotateSpeed)
				elif direction > 2 and direction <= 180.0:
					self.Left(speed = rotateSpeed)
				else:
					self.Direction = 0
					break
			elif position == 1: ### Rotate To Direction 1
				if direction < 88 or direction >= 270.0:
					self.Right(speed = rotateSpeed)
				elif direction > 92 and direction <= 270.0:
					self.Left(speed = rotateSpeed)
				else:
					self.Direction = 1
					break
			elif position == 2: ### Rotate To Direction 2
				if direction < 178:
					self.Right(speed = rotateSpeed)
				elif direction > 182:
					self.Left(speed = rotateSpeed)
				else:
					self.Direction = 2
					break
			else: ### Rotate To Direction 3
				if direction < 268 and direction >= 90.0:
					self.Right(speed = rotateSpeed)
				elif direction > 272 or direction <= 90.0:
					self.Left(speed = rotateSpeed)
				else:
					self.Direction = 3
					break
			
			if loop == False:
				break
		self.Break()
		time.sleep(0.5)


	"""
	### Motor Control ###
	"""

	def Forward(self, speed = 100):
		self.MotorLeft.Forward(speed)
		self.MotorRight.Forward(speed)
		#print "Forward"


	def Backward(self, speed = 100):
		self.MotorLeft.Backward(speed)
		self.MotorRight.Backward(speed)
		#print "Backward"


	def Left(self, speed = 100):
		self.MotorLeft.Backward(speed)
		self.MotorRight.Forward(speed)
		#print "Left"


	def Right(self, speed = 100):
		self.MotorLeft.Forward(speed)
		self.MotorRight.Backward(speed)
		#print "Right"


	def Stop(self, speed = 0):
		self.MotorLeft.Stop(speed)
		self.MotorRight.Stop(speed)
		#print "Stop"


	def Break(self, speed = 100):
		self.MotorLeft.Break(speed)
		self.MotorRight.Break(speed)
		#print "Break"


	def Exit(self):
		GPIO.cleanup()
		print "Exit"
