import time
import RPi.GPIO as GPIO
from arena.tiles import *

from sensor.l298n import *
from sensor.srf04 import *
from sensor.cmps03 import *
from sensor.cmps10 import *
from sensor.kitDropper import *
from sensor.cameraServo import *

import pdb

class Robot():

	#Kit Dropper Pin
	KitDropperPin = 12

	#Camera Servo Pin
	CameraServoPin = 16

	#CMPS10 I2C Adress
	CMPS10_Addr = 0x61

	#MLX90614 I2C Adress
	LeftThermometerAddr = 0x5a
	RightThermometerAddr = 0x2a

	#SRF04 Pins
	BackLeftSonarTRIG = 31
	BackLeftSonarECHO = 32

	FrontLeftSonarTRIG = 29
	FrontLeftSonarECHO = 26

	FrontSonarTRIG = 23
	FrontSonarECHO = 24

	FrontRightSonarTRIG = 21
	FrontRightSonarECHO = 22

	BackRightSonarTRIG = 19
	BackRightSonarECHO = 18


	#Pin1, Pin2, PWM
	motorLeft = [37, 35, 33] #Motor in Left
	motorRight = [40, 38, 36] #Motor in Right

	#Vars
	TileSize = 30.0

	FrontGap = 0.2 #Margin For Robot To Stop in Center of Tile
	FrontDistance = 9.25

	def __init__(self):

		GPIO.setwarnings(False)
		GPIO.setmode(GPIO.BOARD)

		#Tilt Compensated Compass Setup
		self.Compass = CMPS10(self.CMPS10_Addr)

		#Sonar Setup
		self.sonar = []
		
		self.sonar.append(SRF04(self.BackLeftSonarTRIG, self.BackLeftSonarECHO))
		self.sonar.append(SRF04(self.FrontLeftSonarTRIG, self.FrontLeftSonarECHO))
		self.sonar.append(SRF04(self.FrontSonarTRIG, self.FrontSonarECHO)) 
		self.sonar.append(SRF04(self.FrontRightSonarTRIG, self.FrontRightSonarECHO))
		self.sonar.append(SRF04(self.BackRightSonarTRIG, self.BackRightSonarECHO))

		#Motors Setup
		self.MotorLeft = L298N(self.motorLeft[0], self.motorLeft[1], self.motorLeft[2])
		self.MotorRight = L298N(self.motorRight[0], self.motorRight[1], self.motorRight[2])

		#Kit Dropper Setup
		self.KitDropper = KitDropper(self.KitDropperPin)

		#Camera Servo Setup
		self.cameraSevo = CameraServo(self.CameraServoPin)

	"""
	### Functions
	"""

	def MoveTile(self, Ammount = 1, speed = 3):
		(tile, distance) = self.GetTile(self.GetSonar(Sonar.Front))

		if tile > 0:
			finalTile = tile - Ammount
		else:
			finalTile = 0

		while True:

			(tile, distance) = self.GetTile(self.GetSonar(Sonar.Front))

			if tile > finalTile:
				self.Forward(speed)
			elif tile < finalTile:
				self.Backward(speed)
			else:
				if distance < self.FrontDistance - self.FrontGap:
					self.Backward()
				elif distance > self.FrontDistance + self.FrontGap:
					self.Forward()
				else:
					self.Break(speed)
					
					#time.sleep(0.5)

					self.AlignToWall()

					break

	def GetTile(self, distance):
		tile = 0

		while distance >= self.TileSize:
			tile += 1
			distance -= self.TileSize

		if distance > self.TileSize / 3 * 2:
			tile += 1

		return (tile, distance)

	def RotateLeft(self):
		self.Left(5)
		time.sleep(0.6)
		self.Break()

		self.AlignToWall()

	def RotateRight(self):
		self.Right(5)
		time.sleep(0.6)
		self.Break()

		self.AlignToWall()

	def AlignToWall(self):

		speed = 1
		useLeft = False
		useRight = False

		gap = 0.2

		(backLeft, frontLeft, front, frontRight, backRight) = self.GetAllSonar()

		(backLeftTile, backLeftDist) = self.GetTile(backLeft)
		(frontLeftTile, frontLeftDist) = self.GetTile(frontLeft)

		(frontTile, frontDist) =  self.GetTile(frontLeft)

		(backRightTile, backRightDist) = self.GetTile(backRight)
		(frontRightTile, frontRightDist) = self.GetTile(frontRight)

		if frontLeftTile == backLeftTile:
			useLeft = True

		if frontRightTile == backRightTile:
			useRight = True

		if useLeft and useRight:
			if backLeftTile > backRightTile:
				useLeft = False
			elif backLeftTile < backRightTile:
				useRight = False

		while True:

			(backLeft, frontLeft, front, frontRight, backRight) = self.GetAllSonar()

			(backLeftTile, backLeftDist) = self.GetTile(backLeft)
			(frontLeftTile, frontLeftDist) = self.GetTile(frontLeft)

			(frontTile, frontDist) =  self.GetTile(frontLeft)

			(backRightTile, backRightDist) = self.GetTile(backRight)
			(frontRightTile, frontRightDist) = self.GetTile(frontRight)

			if useLeft:
				if backLeftDist > frontLeftDist - gap and backLeftDist < frontLeftDist + gap:
					break
			
			if useRight:
				if backRightDist > frontRightDist - gap and backRightDist < frontRightDist + gap:
					break

			if useLeft == useRight:
				if backLeftDist > frontLeftDist + gap and backRightDist < frontRightDist - gap:
					self.Right(speed)
				elif backLeftDist < frontLeftDist - gap and backRightDist > frontRightDist + gap:
					self.Left(speed)
				elif backLeftDist > frontLeftDist + gap and backRightDist > frontRightDist + gap:
					self.Forward(speed)
				else:
					self.Backward(speed)
			elif useLeft:
				if backLeftDist > frontLeftDist + gap:
					self.Right(speed)
				else: #elif backLeftDist < frontLeftDist - gap:
					self.Left(speed)
			else:
				if backRightDist < frontRightDist - gap:
					self.Right(speed)
				else: #elif backRightDist > frontRightDist + gap:
					self.Left(speed)

		self.Break()
		#time.sleep(0.5)

	def GetWalls(self):
		(backLeft, frontLeft, front, frontRight, backRight) = self.GetAllSonar()

		wallLeft = True
		wallFront = True
		wallRight = True

		gap = self.TileSize

		if backLeft > gap and frontLeft > gap:
			wallLeft = False

		if front > gap:
			wallFront = False

		if backRight > gap and frontRight > gap:
			wallRight = False

		return (wallLeft, wallFront, wallRight)


	"""
	### Sensors
	"""

	def GetAllSonar(self):
		return (self.GetSonar(Sonar.BackLeft), self.GetSonar(Sonar.FrontLeft), self.GetSonar(Sonar.Front), self.GetSonar(Sonar.FrontRight), self.GetSonar(Sonar.BackRight))

	def GetSonar(self, sonar = Sonar.Front):

		distance = self.sonar[sonar].getCM()

		return distance

	"""
	### Motor Control ###
	"""

	def MotorSpeedCalibration(self, speed):
		mLeft = 0
		mRight = 0

		if speed == 1:
			mLeft = 20
			mRight = 20
		elif speed == 2:
			mLeft = 40
			mRight = 40
		elif speed == 3:
			mLeft = 60
			mRight = 60
		elif speed == 4:
			mLeft = 80
			mRight = 80
		elif speed == 5:
			mLeft = 100
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