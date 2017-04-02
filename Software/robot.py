import time
import RPi.GPIO as GPIO

from sensor.l298n import L298N
from sensor.srf04 import SRF04
from sensor.cmps03 import CMPS03
from sensor.cmps10 import CMPS10

class Robot():

	#CMPS03
	CMPS03_Addr = 0x60

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
	motorLeft = [37, 35, 33] #Motor in Left
	motorRight = [40, 38, 36] #Motor in Right

	#Vars
	TileSize = 30.0
	Direction = 0 # Compass Direction: 0, North; 1, East; 2, South; 3, West

	def __init__(self):

		GPIO.setwarnings(False)
		GPIO.setmode(GPIO.BOARD)

		#Compass Setup
		self.compass = CMPS03(self.CMPS03_Addr)

		#Tilt Compensated Compass Setup
		self.tiltCompass = CMPS10(self.CMPS10_Addr)

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
	### Functions
	"""

	def MoveTile(self):
		(tile, distance) = self.GetTile(self.GetSonar())

		if tile > 0:
			finalTile = tile - 1
		else:
			finalTile = 0

		positionGap = 0.25 #Margin For Robot To Stop in Center of Tile
		frontDistance = (self.TileSize / 2) - 7.0

		while True:

			(tile, distance) = self.GetTile(self.GetSonar())

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

					break

	def GetTile(self, distance):
		tile = 0

		while distance >= self.TileSize:
			tile += 1
			distance -= self.TileSize

		return (tile, distance)

	def RotateLeft(self):

		if self.Direction == 1:
			self.Rotate(0)
		elif self.Direction == 2:
			self.Rotate(1)
		elif self.Direction == 3:
			self.Rotate(2)
		elif self.Direction == 0:
			self.Rotate(3)

	def RotateRight(self):
		
		if self.Direction == 1:
			self.Rotate(2)
		elif self.Direction == 2:
			self.Rotate(3)
		elif self.Direction == 3:
			self.Rotate(0)
		elif self.Direction == 0:
			self.Rotate(1)

	def Rotate(self, position, loop = True, margin = 1):

		rotateSpeed = 2

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
				if direction < 70 - margin or direction >= 270.0:
					self.Right(speed = rotateSpeed)
				elif direction > 70 + margin and direction <= 270.0:
					self.Left(speed = rotateSpeed)
				else:
					self.Direction = 1
					break
			elif position == 2: ### Rotate To Direction 2
				if direction < 190 - margin:
					self.Right(speed = rotateSpeed)
				elif direction > 190.0 + margin:
					self.Left(speed = rotateSpeed)
				else:
					self.Direction = 2
					break
			else: ### Rotate To Direction 3
				if direction < 290.0 - margin and direction >= 90.0:
					self.Right(speed = rotateSpeed)
				elif direction > 290.0 + margin or direction <= 90.0:
					self.Left(speed = rotateSpeed)
				else:
					self.Direction = 3
					break
			
			if loop == False:
				break

		self.Break()
		time.sleep(0.5)

	def GetWalls(self):
		sonarLeft = self.GetSonar("Left")
		sonarFront = self.GetSonar("Front")
		sonarRight = self.GetSonar("Right")

		wallLeft = True
		wallFront = True
		wallRight = True

		gap = self.TileSize/3 * 2

		if sonarLeft > gap:
			wallLeft = False

		if sonarFront > gap:
			wallFront = False

		if sonarRight > gap:
			wallRight = False

		return (wallLeft, wallFront, wallRight)


	"""
	### Sensors
	"""

	def GetBearing(self):
		bearing = self.compass.bearing3599()

		bearing -= self.CompassOffset

		if bearing > 360.0:
			bearing -= 360.0
		elif bearing < 0.0:
			bearing += 360.0

		return bearing

	def GetSonar(self, direction = "Front"):

		direction = direction.lower()
		sonarNumber = 0

		if direction == "left":
			sonarNumber = 0
		elif direction == "right":
			sonarNumber = 2
		else: # Front Sonar
			sonarNumber = 1

		distance = self.sonar[sonarNumber].getCM()

		return distance

	"""
	### Motor Control ###
	"""

	def MotorSpeedCalibration(self, speed):
		mLeft = 0
		mRight = 0

		if speed == 1:
			mLeft = 19
			mRight = 20
		elif speed == 2:
			mLeft = 35
			mRight = 40
		elif speed == 3:
			mLeft = 50
			mRight = 60
		elif speed == 4:
			mLeft = 65
			mRight = 80
		elif speed == 5:
			mLeft = 80
			mRight = 100

		return (mLeft, mRight)

	def Forward(self, speed = 3):
		(speedLeft, speedRight) = self.MotorSpeedCalibration(speed)
		self.MotorLeft.Forward(speedLeft)
		self.MotorRight.Forward(speedRight)


	def Backward(self, speed = 3):
		(speedLeft, speedRight) = self.MotorSpeedCalibration(speed)
		self.MotorLeft.Backward(speedLeft)
		self.MotorRight.Backward(speedRight)


	def Left(self, speed = 2):
		(speedLeft, speedRight) = self.MotorSpeedCalibration(speed)
		self.MotorLeft.Backward(speedLeft)
		self.MotorRight.Forward(speedRight)


	def Right(self, speed = 2):
		(speedLeft, speedRight) = self.MotorSpeedCalibration(speed)
		self.MotorLeft.Forward(speedLeft)
		self.MotorRight.Backward(speedRight)


	def Stop(self, speed = 0):
		(speedLeft, speedRight) = self.MotorSpeedCalibration(speed)
		self.MotorLeft.Stop(speedLeft)
		self.MotorRight.Stop(speedRight)


	def Break(self, speed = 5):
		(speedLeft, speedRight) = self.MotorSpeedCalibration(speed)
		self.MotorLeft.Break(speedLeft)
		self.MotorRight.Break(speedRight)


	def Exit(self):
		GPIO.cleanup()