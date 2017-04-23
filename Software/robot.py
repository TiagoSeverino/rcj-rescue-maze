import time
import RPi.GPIO as GPIO
from arena.tiles import *

from sensor.l298n import *
from sensor.srf04 import *
from sensor.cmps03 import *
from sensor.cmps10 import *
from sensor.mlx90614 import *
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
	LeftThermometerAddr = 0x2a
	RightThermometerAddr = 0x5a

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

	#Self Calibration
	BearOffSet = 0
	PichOffSet = 0
	RollOffSet = 0

	#Vars
	TileSize = 30.0

	FrontGap = 0.4 #Margin For Robot To Stop in Center of Tile
	FrontDistance = 9.75

	def __init__(self):

		GPIO.setwarnings(False)
		GPIO.setmode(GPIO.BOARD)

		#Tilt Compensated Compass Setup
		self.compass = CMPS10(self.CMPS10_Addr)

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

		#Thermometer Setup		
		self.thermometerLeft = MLX90614(self.LeftThermometerAddr)		
		self.thermometerRight = MLX90614(self.RightThermometerAddr)

	"""
	### Functions
	"""

	def MoveTile(self, Ammount = 1, CheckVictims = True):
		(tile, distance) = self.GetTile(self.GetSonar(Sonar.Front))

		finalTile = tile - Ammount

		if finalTile < 0:
			finalTile = 0
			
		gap = 0.1

		CheckVictimLeft = CheckVictims
		CheckVictimRight = CheckVictims

		while True:

			if CheckVictimLeft:
				if self.IsVictimLeft():
					CheckVictimLeft = False
			
			if CheckVictimRight:
				if self.IsVictimRight():
					CheckVictimRight = False

			(tile, distance) =  self.GetTile(self.GetSonar(Sonar.Front))

			inclination = self.GetPich()

			if (inclination > 10 and inclination < 40) or (inclination > 220 and inclination < 245):
				finalTile = 0

			if tile > finalTile or distance > self.FrontDistance + self.FrontGap:

				(frontLeftTile, frontLeftDist) = self.GetTile(self.GetSonar(Sonar.FrontLeft))
				(frontRightTile, frontRightDist) = self.GetTile(self.GetSonar(Sonar.FrontRight))

				if frontLeftDist > frontRightDist + gap:
					self.Forward1(70, 100)
				elif frontLeftDist < frontRightDist - gap:
					self.Forward1(100, 80)
				else:
					self.Forward(3)
				
			elif tile < finalTile or distance < self.FrontDistance - self.FrontGap:

				(backLeftTile, backLeftDist) = self.GetTile(self.GetSonar(Sonar.BackLeft))
				(backRightTile, backRightDist) = self.GetTile(self.GetSonar(Sonar.BackRight))

				if backLeftDist > backRightDist + gap:
					self.Backward1(30, 65)
				elif backLeftDist < backRightDist - gap:
					self.Backward1(55, 35)
				else:
					self.Backward(3)
			else:
				self.Break()
				time.sleep(0.1)
				self.AlignToWall()
				break

	def GetTile(self, distance):
		tile = 0

		while distance >= self.TileSize:
			tile += 1
			distance -= self.TileSize

		return (tile, distance)

	def RotateLeft(self):
		self.Left(5)
		time.sleep(0.75)
		self.Break()

		self.AlignToWall()

	def RotateRight(self):
		self.Right(5)
		time.sleep(0.75)
		self.Break()

		self.AlignToWall()

	def AlignToWall(self):

		speed = 2
		useLeft = False
		useRight = False

		gap = 0.15

		(backLeft, frontLeft, frontRight, backRight) = (self.GetSonar(Sonar.BackLeft), self.GetSonar(Sonar.FrontLeft), self.GetSonar(Sonar.FrontRight), self.GetSonar(Sonar.BackRight))

		(backLeftTile, backLeftDist) = self.GetTile(backLeft)
		(frontLeftTile, frontLeftDist) = self.GetTile(frontLeft)

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

			if useLeft == useRight:
				(backLeft, frontLeft, frontRight, backRight) = (self.GetSonar(Sonar.BackLeft), self.GetSonar(Sonar.FrontLeft), self.GetSonar(Sonar.FrontRight), self.GetSonar(Sonar.BackRight))

				(backLeftTile, backLeftDist) = self.GetTile(backLeft)
				(frontLeftTile, frontLeftDist) = self.GetTile(frontLeft)

				(backRightTile, backRightDist) = self.GetTile(backRight)
				(frontRightTile, frontRightDist) = self.GetTile(frontRight)
			elif useLeft:
				(backLeft, frontLeft) = (self.GetSonar(Sonar.BackLeft), self.GetSonar(Sonar.FrontLeft))

				(backLeftTile, backLeftDist) = self.GetTile(backLeft)
				(frontLeftTile, frontLeftDist) = self.GetTile(frontLeft)
			else:
				(frontRight, backRight) = (self.GetSonar(Sonar.FrontRight), self.GetSonar(Sonar.BackRight))

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
		time.sleep(0.1)

	def GetWalls(self):
		(backLeft, frontLeft, front, frontRight, backRight) = self.GetAllSonar()

		wallLeft = False
		wallFront = False
		wallRight = False

		gap = self.TileSize

		if backLeft < gap or frontLeft < gap:
			wallLeft = True

		if front < gap:
			wallFront = True

		if backRight < gap or frontRight < gap:
			wallRight = True

		return (wallLeft, wallFront, wallRight)


	def DropKit(self, ammount=1):
		self.Break()
		time.sleep(0.1)
		self.KitDropper.drop(ammount)
		time.sleep(0.1)

	def IsVictimLeft(self):
		tempGap = 5.0

		(ambLeft, objLeft) = self.GetTemperatureLeft()

		if (objLeft - ambLeft) > tempGap:
			self.RotateRight()
			self.DropKit()
			self.RotateLeft()
			print "Victim Detected"
			return True
		else:
			return False

	def IsVictimRight(self):
		tempGap = 5.0

		(ambRight, objRight) = self.GetTemperatureRight()

		if (objRight - ambRight) > tempGap:
			self.RotateLeft()
			self.DropKit()
			self.RotateRight()
			print "Victim Detected"
			return True
		else:
			return False

	"""
	### Sensors
	"""

	def GetAllSonar(self):
		return (self.GetSonar(Sonar.BackLeft), self.GetSonar(Sonar.FrontLeft), self.GetSonar(Sonar.Front), self.GetSonar(Sonar.FrontRight), self.GetSonar(Sonar.BackRight))

	def GetSonar(self, sonar = Sonar.Front):

		distance = self.sonar[sonar].getCM()

		return 
		
	def GetBear(self):
		bear = self.compass.bearing255()

		bear -= self.BearOffSet
 
 		if bear > 255:
 			bear -= 255
 		elif bear < 0:
 			bear += 255

  		return bear

	def GetPich(self):
		pich = self.compass.pich()

		pich -= self.PichOffSet
 
 		if pich > 255:
 			pich -= 255
 		elif pich < 0:
 			pich += 255

  		return pich

	def GetRoll(self):		
		roll = self.compass.roll()

		roll -= self.RollOffSet
 
 		if roll > 255:
 			roll -= 255
 		elif roll < 0:
 			roll += 255

  		return roll

	def GetTemperatureLeft(self):
		self.ambTempLeft = self.thermometerLeft.get_amb_temp()
		self.objTempLeft = self.thermometerLeft.get_obj_temp()		

		return (self.ambTempLeft, self.objTempLeft)


	def GetTemperatureRight(self):
		self.ambTempRight = self.thermometerRight.get_amb_temp()
		self.objTempRight = self.thermometerRight.get_obj_temp()		

		return (self.ambTempRight, self.objTempRight)

	"""
	### Motor Control ###
	"""

	def MotorSpeedCalibration(self, speed):
		mLeft = 0
		mRight = 0

		if speed == 1:
			mLeft = 17
			mRight = 21
		elif speed == 2:
			mLeft = 30
			mRight = 40
		elif speed == 3:
			mLeft = 43
			mRight = 60
		elif speed == 4:
			mLeft = 60
			mRight = 80
		elif speed == 5:
			mLeft = 78
			mRight = 100

		return (mLeft, mRight)

	def Forward(self, speed = 3):
		(speedLeft, speedRight) = self.MotorSpeedCalibration(speed)
		self.MotorLeft.Forward(speedLeft)
		self.MotorRight.Forward(speedRight)

	def Forward1(self, speedLeft, speedRight):
		self.MotorLeft.Forward(speedLeft)
		self.MotorRight.Forward(speedRight)

	def Backward(self, speed = 2):
		(speedLeft, speedRight) = self.MotorSpeedCalibration(speed)
		self.MotorLeft.Backward(speedLeft)
		self.MotorRight.Backward(speedRight)

	def Backward1(self, speedLeft, speedRight):
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