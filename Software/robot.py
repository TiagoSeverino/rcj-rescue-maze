import time
import RPi.GPIO as GPIO

from lib.l298n import L298N
from lib.srf04 import SRF04
from lib.cmps10 import CMPS10
from lib.cmps03 import CMPS03
from lib.camera import Camera
from lib.mlx90614 import MLX90614
from lib.kitDropper import KitDropper
from lib.cameraServo import CameraServo

class Robot():

	#Kit Dropper Servo
	KitDropperPin = 7

	#Camera Servo
	CameraServoPin = 9

	#Camera Resolution
	CameraWidth = 208
	CameraHeight = 160

	#CMPS03
	CMPS03_Addr = 0x61

	#CMPS10
	CMPS10_Addr = 0x61

	#MLX90614
	LeftThermometerAddr = 0x5a
	RightThermometerAddr = 0x2a

	#SRF04
	LeftSonarTRIG = 19
	LeftSonarECHO = 11

	FrontSonarTRIG = 21
	FrontSonarECHO = 13

	RightSonarTRIG = 23
	RightSonarECHO = 15

	#Pin1, Pin2, PWM
	motorLeft = [38, 40, 36] #Motor in Left
	motorRight = [35, 37, 33] #Motor in Right

	#Vars

	#Arena Vars
	SonarOffSetV = 14.0 #Vertical distance between center of robot and front sonars
	SonarOffSetH = 4.0 #Horizontal distance between center of robot and side sonars
	TileSize = 30.0 #Gap Between

	#Localization Vars
	Direction = 0


	def __init__(self):

		GPIO.setwarnings(False)
		GPIO.setmode(GPIO.BOARD)

		#Kit Dropper Servo Setup
		self.kitDropper = KitDropper(self.KitDropperPin)

		#Camera Servo Setup
		self.cameraServo = CameraServo(self.CameraServoPin)

		#Camera Setup
		self.camera = Camera(width = self.CameraWidth, height = self.CameraHeight)

		#Compass Setup
		self.compass = CMPS03(self.CMPS03_Addr)

		#Tilt Compensated Compass Setup
		self.tiltCompass = CMPS10(self.CMPS10_Addr)

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

	def SonarToID(direction):
		direction = direction.lower()

		if direction == "left":
			return 0
		elif direction == "right":
			return 2
		else: # Front Sonar
			return 1

	def GetSonar(self, direction = "Front"):

		distance = self.sonar[self.SonarToID(direction)].getCM()

		return distance

	def IsWall(self, direction = "Front"):
		distance = self.GetSonar(direction)

		if distance > self.TileSize:
			return False
		else:
			return True

	def DropKit(self, ammount=1):
		self.Break()
		time.sleep(0.1)
		self.kitDropper.drop(ammount)
		print "Dropped", ammount, " kits!"


	def GetBearing(self):
		bearing = self.compass.bearing3599()

		bearing -= self.CompassOffset

		if bearing > 360.0:
			bearing -= 360.0
		elif bearing < 0.0:
			bearing += 360.0

		return bearing

	def GetTiltBearing(self):
		bearing = self.tiltCompass.bearing3599()

		bearing -= self.CompassOffset

		if bearing > 360.0:
			bearing -= 360.0
		elif bearing < 0.0:
			bearing += 360.0

		return bearing

	def GetPich(self):
		pich = self.tiltCompass.pich()

		return pich


	def GetRoll(self):
		roll = self.tiltCompass.roll()

		return roll


	def GetTemperatureLeft(self):
		self.ambTempLeft = self.thermometerLeft.get_amb_temp()

		time.sleep(0.00001)

		self.objTempLeft = self.thermometerLeft.get_obj_temp()

		return (self.ambTempLeft, self.objTempLeft)


	def GetTemperatureRight(self):
		self.ambTempRight = self.thermometerRight.get_amb_temp()

		time.sleep(0.00001)

		self.objTempRight = self.thermometerRight.get_obj_temp()

		return (self.ambTempRight, self.objTempRight)

	def IsVictim(self):

		tempGap = 10

		(ambLeft, objLeft) = self.GetTemperatureLeft()

		time.sleep(0.00001)

		(ambRight, objRight) = self.GetTemperatureRight()

		if (objLeft - ambLeft) > tempGap or (objRight - ambRight) > tempGap:
			print "Victim Detected!"
			return True

		return False

	"""
	### Precise Moving ###
	"""

	def GetTile(self, distance):
		tile = 0

		while distance >= self.TileSize:
			tile += 1
			distance -= self.TileSize

		return (tile, distance)

	def MoveTile(self):
		(tile, distance) = self.GetTile(self.GetSonar())

		if tile > 0:
			finalTile = tile - 1
		else:
			finalTile = 0

		positionGap = 1.0 #Margin For Robot To Stop in Center of Tile
		frontDistance = (self.TileSize / 2) + self.SonarOffSetV

		while True:

			(tile, distance) = self.GetTile(self.GetSonar())

			if self.IsVictim():
				self.DropKit()

			if tile > finalTile:
				self.Forward()
			elif tile < finalTile:
				self.Backward()
			else:
				if distance < frontDistance - positionGap:
					self.Backward()
				elif distance > frontDistance + positionGap:
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

	def Rotate(self, position, loop = True, margin = 2):

		rotateSpeed = 60

		while True:
			
			direction = self.GetBearing()
			

			if position == 0: ### Rotate To Direction 0
				if direction < 360.0 - margin and direction >= 180.0:
					self.Right(speed = rotateSpeed)
				elif direction > 0 + margin and direction <= 180.0:
					self.Left(speed = rotateSpeed)
				else:
					self.Direction = 0
					break
			elif position == 1: ### Rotate To Direction 1
				if direction < 90 - margin or direction >= 270.0:
					self.Right(speed = rotateSpeed)
				elif direction > 90 + margin and direction <= 270.0:
					self.Left(speed = rotateSpeed)
				else:
					self.Direction = 1
					break
			elif position == 2: ### Rotate To Direction 2
				if direction < 180 - margin:
					self.Right(speed = rotateSpeed)
				elif direction > 180.0 + margin:
					self.Left(speed = rotateSpeed)
				else:
					self.Direction = 2
					break
			else: ### Rotate To Direction 3
				if direction < 270.0 - margin and direction >= 90.0:
					self.Right(speed = rotateSpeed)
				elif direction > 270.0 + margin or direction <= 90.0:
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


	def Backward(self, speed = 100):
		self.MotorLeft.Backward(speed)
		self.MotorRight.Backward(speed)


	def Left(self, speed = 100):
		self.MotorLeft.Backward(speed)
		self.MotorRight.Forward(speed)


	def Right(self, speed = 100):
		self.MotorLeft.Forward(speed)
		self.MotorRight.Backward(speed)


	def Stop(self, speed = 0):
		self.MotorLeft.Stop(speed)
		self.MotorRight.Stop(speed)


	def Break(self, speed = 100):
		self.MotorLeft.Break(speed)
		self.MotorRight.Break(speed)


	def Exit(self):
		GPIO.cleanup()
		print "Exit"
