import time
import RPi.GPIO as GPIO

from lib.motor import Motor
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

	#Pin1, Pin2
	motorLeft = [35, 37] #Motor in Left
	motorRight = [38, 40] #Motor in Right
	
	#Vars
	
	#Arena Vars
	Lenght = 22.0
	Width = 13.0
	TileSize =30.0

	#Localization Vars
	Direction = 0


	def __init__(self):
		
		GPIO.setmode(GPIO.BOARD)
		#GPIO.setwarnings(False)

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
		self.sonarLeft = SRF04(self.LeftSonarTRIG, self.LeftSonarECHO)
		self.sonarFront = SRF04(self.FrontSonarTRIG, self.FrontSonarECHO)
		self.sonarRight = SRF04(self.RightSonarTRIG, self.RightSonarECHO)

		#Motors Setup
		self.MotorLeft = Motor(self.motorLeft[0], self.motorLeft[1])
		self.MotorRight = Motor(self.motorRight[0], self.motorRight[1])


		#Register Position
		self.CompassOffset = self.compass.bearing3599()


	def GetLeftSonar(self):

		distance = self.sonarLeft.raw_distance()
		print "Left Sonar: ", distance

		return distance


	def GetFrontSonar(self):

		distance = self.sonarFront.raw_distance()
		print "Front Sonar: ", distance

		return distance


	def GetRightSonar(self):

		distance = self.sonarRight.raw_distance()
		print "Right Sonar: ", distance

		return distance


	def DropKit(self, ammount = 1):
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
		
		print "Bearing: ", bearing

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

	def RotateLeft(self):

		if self.Direction > 1:
			FinalDirection = (self.Direction - 1) * 90

			while True:
				direction = self.GetBearing()
				if direction > FinalDirection + 2.5:
					self.Left()
				elif direction < FinalDirection - 2.5:
					self.Right()
				else:
					self.Direction += 1
					self.Break()
					break
		elif self.Direction == 0:
			while True:
				direction = self.GetBearing()
				if direction <= 90.0 or direction > 272.5:
					self.Left()
				elif direction >= 90.0 and direction < 267.7:
					self.Right()
				else:
					self.Direction = 3
					self.Break()
					break
		else: # self.Direction == 1:
			while True:
				direction = self.GetBearing()
				if direction > 2.5 and direction <= 180.0:
					self.Left()
				elif direction < 357.5 and direction >= 180.0:
					self.Right()
				else:
					self.Direction = 0
					self.Break()
					break

		print "Rotated Left!"

	def RotateRight(self):

		if self.Direction < 3 and self.Direction != 0:
			FinalDirection = (self.Direction - 3) * 90

			while True:
				direction = self.GetBearing()
				if direction > FinalDirection + 2.5:
					self.Left()
				elif direction < FinalDirection - 2.5:
					self.Right()
				else:
					self.Direction += 1
					self.Break()
					break
		elif self.Direction == 0:
			while True:
				direction = self.GetBearing()
				if direction < 87.5 or direction >= 270.0:
					self.Right()
				elif direction > 92.5 and direction <= 270.0:
					self.Left()
				else:
					self.Direction = 1
					self.Break()
					break
		else: # self.Direction == 3:
			while True:
				direction = self.GetBearing()
				if direction > 2.5 and direction <= 180.0:
					self.Left()
				elif direction < 357.5 and direction >= 180.0:
					self.Right()
				else:
					self.Direction = 0
					self.Break()
					break

		print "Rotated Right!"


	def Forward(self):
		self.MotorLeft.Forward()
		self.MotorRight.Forward()
		print "Forward"


	def Backward(self):
		self.MotorLeft.Backward()
		self.MotorRight.Backward()
		print "Backward"


	def Left(self):
		self.MotorLeft.Backward()
		self.MotorRight.Forward()
		print "Left"


	def Right(self):
		self.MotorLeft.Forward()
		self.MotorRight.Backward()
		print "Right"


	def Stop(self):
		self.MotorLeft.Stop()
		self.MotorRight.Stop()
		print "Stop"


	def Break(self):
		self.MotorLeft.Break()
		self.MotorRight.Break()
		print "Break"


	def Exit(self):
		GPIO.cleanup()
		print "Exit"
