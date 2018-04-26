import time
import RPi.GPIO as GPIO
from arena.tiles import *
from RPIO import PWM
from sensor.led import *
from sensor.laser import *
from sensor.l298n.l298n import *
from sensor.cmps10.cmps10 import *
from sensor.switch import *
from sensor.tpa81.tpa81 import *
from sensor.lineSensor import *

import pdb

class Robot():

	#Kit Dropper Pin
	KitDropperPin = 24

	#Front Touch Switches
	LeftSwitch = 16
	RightSwitch = 12

	#Line Sensor Pin
	LineSensorPin = 22

	#CMPS10 I2C Adress
	CMPS10_Addr = 0x61

	#TPA81 I2C Adress
	LeftThermometerAddr = 0x68
	RightThermometerAddr = 0x69

	#Pin1, Pin2, PWM
	motorLeft = [38, 40, 36] #Motor in Left
	motorRight = [26, 32, 24] #Motor in Right

	#Self Calibration
	BearOffSet = 0
	Bear3599OffSet = 0
	PitchOffSet = 0
	RollOffSet = 0

	#Vars
	TileSize = 32.5

	FrontGap = 0.3 #Margin For Robot To Stop in Center of Tile
	FrontDistance = 6.25
	AlignGap = 0.05

	MinTempGap = 4.0
	MinVictimTemp = 26

	#Kit Dropper Settings
	LeftPos = 1750
	FrontPosL = 1280
	FrontPosR = 1450
	RightPos = 1000
	Time90Deg = 0.75

	ramp = False

	tile = 0

	def __init__(self):

		GPIO.setwarnings(False)
		GPIO.setmode(GPIO.BOARD)

		#Tilt Compensated Compass Setup
		self.compass = CMPS10(self.CMPS10_Addr)

		#Motors Setup
		self.MotorLeft = L298N(self.motorLeft[0], self.motorLeft[1], self.motorLeft[2])
		self.MotorRight = L298N(self.motorRight[0], self.motorRight[1], self.motorRight[2])

		#Lasers Setup
		self.Lasers = Lasers(7, 11, 13, 15, 19)

		#Line Sensor Setup
		self.lineSensor = LineSensor(self.LineSensorPin)

		#Thermometer Setup
		self.thermometerLeft = TPA81(self.LeftThermometerAddr)
		self.thermometerRight = TPA81(self.RightThermometerAddr)

		#Touch Switc Setup
		self.leftSwitch = SWITCH(self.LeftSwitch)
		self.rightSwitch = SWITCH(self.RightSwitch)

	"""
	### Functions
	"""

	def MoveTile(self, Ammount = 1, CheckVictims = False):
		(tile, distance) = self.GetTile(self.GetLaser(Laser.Front))

		if distance >= (self.TileSize - (self.TileSize / 2.5)):
			tile += 1
			distance = 0

		finalTile = tile - Ammount

		if finalTile < 0:
			finalTile = 0

		gap = 0.05

		while True:

			(tile, distance) =  self.GetTile(self.GetLaser(Laser.Front))

			inclination = self.GetPitch()

			if (inclination > 15 and inclination < 40) or (inclination > 215 and inclination < 240):
				self.ramp = True
				finalTile = 0

			if tile > finalTile or (tile == finalTile and distance > self.FrontDistance + self.FrontGap):

				(frontLeftTile, frontLeftDist) = self.GetTile(self.GetLaser(Laser.FrontLeft))
				(frontRightTile, frontRightDist) = self.GetTile(self.GetLaser(Laser.FrontRight))

				if frontLeftDist > frontRightDist + gap:
					if self.ramp == False or inclination < 40 or inclination > 240:
						self.Forward1(40, 50)
					else:
						self.Forward1(70, 100)
				elif frontLeftDist < frontRightDist - gap:
					if self.ramp == False or inclination < 40 or inclination > 240:
						self.Forward1(50, 40)
					else:
						self.Forward1(100, 70)
				else:
					if self.ramp == False or inclination < 40 or inclination > 240:
						self.Forward(3)
					else:
						self.Forward(5)

				if not self.ramp:
					if self.leftSwitch.IsOn():
						self.Backward(2)
						time.sleep(0.3)
						self.Left(2)
						time.sleep(0.3)
						self.Backward(2)
						time.sleep(0.3)
						self.Right(2)
						time.sleep(0.45)
					elif self.rightSwitch.IsOn():
						self.Backward(2)
						time.sleep(0.3)
						self.Right(2)
						time.sleep(0.3)
						self.Backward(2)
						time.sleep(0.3)
						self.Left(2)
						time.sleep(0.45)

			elif tile < finalTile or (tile == finalTile and distance < self.FrontDistance - self.FrontGap):

				(backLeftTile, backLeftDist) = self.GetTile(self.GetLaser(Laser.BackLeft))
				(backRightTile, backRightDist) = self.GetTile(self.GetLaser(Laser.BackRight))

				if backLeftDist > backRightDist + gap:
					self.Backward1(40, 50)
				elif backLeftDist < backRightDist - gap:
					self.Backward1(50, 40)
				else:
					self.Backward(3)

				if self.leftSwitch.IsOn() and self.rightSwitch.IsOn():
					(finalTile, distance) = self.GetTile(self.GetLaser(Laser.Front))
					
			else:
				self.Break()
				time.sleep(0.1)
				self.AlignToWall()

				(wallLeft, wallFront, wallRight) = self.GetWalls()

				if CheckVictims and wallLeft:
					self.IsVictimLeft()

				if CheckVictims and wallRight:
					self.IsVictimRight()

				break

	def GetTile(self, distance):
		tile = 0

		while distance >= self.TileSize:
			tile += 1
			distance -= self.TileSize

		return (tile, distance)

	def RotateLeft(self, CheckVictims = False):
		self.Left(5)
		time.sleep(0.55)
		self.Break()

		self.AlignToWall()

		(wallLeft, wallFront, wallRight) = self.GetWalls()

		if CheckVictims and wallLeft:
			self.IsVictimLeft()

		if CheckVictims and wallRight:
			self.IsVictimRight()

	def RotateRight(self, CheckVictims = False):
		self.Right(5)
		time.sleep(0.55)
		self.Break()

		self.AlignToWall()

		(wallLeft, wallFront, wallRight) = self.GetWalls()

		if CheckVictims and wallLeft:
			self.IsVictimLeft()

		if CheckVictims and wallRight:
			self.IsVictimRight()

	def AlignToWall(self):

		speed = 1
		useLeft = False
		useRight = False

		(backLeft, frontLeft, frontRight, backRight) = (self.GetLaser(Laser.BackLeft), self.GetLaser(Laser.FrontLeft), self.GetLaser(Laser.FrontRight), self.GetLaser(Laser.BackRight))

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

		if useLeft == False and useRight == False:
			useLeft = True

		i = 0

		while True:
			i += 1

			if i > 60:
				break
				
			if useLeft == useRight:
				(backLeft, frontLeft, frontRight, backRight) = (self.GetLaser(Laser.BackLeft), self.GetLaser(Laser.FrontLeft), self.GetLaser(Laser.FrontRight), self.GetLaser(Laser.BackRight))

				(backLeftTile, backLeftDist) = self.GetTile(backLeft)
				(frontLeftTile, frontLeftDist) = self.GetTile(frontLeft)

				(backRightTile, backRightDist) = self.GetTile(backRight)
				(frontRightTile, frontRightDist) = self.GetTile(frontRight)
			elif useLeft:
				(backLeft, frontLeft) = (self.GetLaser(Laser.BackLeft), self.GetLaser(Laser.FrontLeft))

				(backLeftTile, backLeftDist) = self.GetTile(backLeft)
				(frontLeftTile, frontLeftDist) = self.GetTile(frontLeft)
			else:
				(frontRight, backRight) = (self.GetLaser(Laser.FrontRight), self.GetLaser(Laser.BackRight))

				(backRightTile, backRightDist) = self.GetTile(backRight)
				(frontRightTile, frontRightDist) = self.GetTile(frontRight)

			gap = self.AlignGap

			if useLeft:
				gap = self.AlignGap * (frontLeftTile * 1.25 + 1)
				if backLeftDist > frontLeftDist - gap and backLeftDist < frontLeftDist + gap:
					break

			if useRight:
				gap *= self.AlignGap * (frontRightTile * 1.25 + 1)
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
		(backLeft, frontLeft, front, frontRight, backRight) = self.GetAllLaser()

		wallLeft = False
		wallFront = False
		wallRight = False

		gap = self.TileSize / 1.75

		if backLeft < gap and frontLeft < gap:
			wallLeft = True

		if front < gap:
			wallFront = True

		if backRight < gap and frontRight < gap:
			wallRight = True

		return (wallLeft, wallFront, wallRight)


	def DropKit(self, position, ammount = 1):
		self.Break()
		time.sleep(0.1)

		servo = PWM.Servo()

		for x in range(0, ammount):
			if position == 0:
				servo.set_servo(self.KitDropperPin, self.LeftPos)
				time.sleep(self.Time90Deg)
				servo.set_servo(self.KitDropperPin, self.FrontPosL)

			elif position == 1:
				servo.set_servo(self.KitDropperPin, self.RightPos)
				time.sleep(self.Time90Deg)
				servo.set_servo(self.KitDropperPin, self.FrontPosR)

			time.sleep(self.Time90Deg)
		#servo.cleanup()
		time.sleep(0.1)

	def IsVictimLeft(self):
		(ambLeft, objLeft) = self.GetTemperatureLeft()

		if ((objLeft - ambLeft) > self.MinTempGap) and objLeft > self.MinVictimTemp:
			self.DropKit(position = 0)
			print "Victim Detected"
			return True
		else:
			return False

	def IsVictimRight(self):
		(ambRight, objRight) = self.GetTemperatureRight()

		if ((objRight - ambRight) > self.MinTempGap) and objRight > self.MinVictimTemp:
			self.DropKit(position = 1)
			print "Victim Detected"
			return True
		else:
			return False

	"""
	### Sensors
	"""

	def GetAllLaser(self):
		return (self.GetLaser(Laser.BackLeft), self.GetLaser(Laser.FrontLeft), self.GetLaser(Laser.Front), self.GetLaser(Laser.FrontRight), self.GetLaser(Laser.BackRight))

	def GetLaser(self, laser = Laser.Front):
		distance = self.Lasers.getCM(laser)
		return distance

	def GetBear(self):
		bear = self.compass.bearing255()

		bear -= self.BearOffSet

 		if bear > 255:
 			bear -= 255
 		elif bear < 0:
 			bear += 255

  		return bear

	def GetBear3599(self):
		bear = self.compass.bearing3599()

		bear -= self.Bear3599OffSet

 		if bear > 360.0:
 			bear -= 360.0
 		elif bear < 360.0:
 			bear += 360.0

  		return bear

	def GetPitch(self):
		pitch = self.compass.pitch()

		pitch -= self.PitchOffSet

 		if pitch > 255:
 			pitch -= 255
 		elif pitch < 0:
 			pitch += 255

  		return pitch

	def GetRoll(self):
		roll = self.compass.roll()

		roll -= self.RollOffSet

 		if roll > 255:
 			roll -= 255
 		elif roll < 0:
 			roll += 255

  		return roll

	def GetTemperatureLeft(self):
		self.ambTempLeft = self.thermometerLeft.ambientTemperature()
		self.objTempLeft = self.thermometerLeft.highestTemp()

		return (self.ambTempLeft, self.objTempLeft)


	def GetTemperatureRight(self):
		self.ambTempRight = self.thermometerRight.ambientTemperature()
		self.objTempRight = self.thermometerRight.highestTemp()

		return (self.ambTempRight, self.objTempRight)

	def GetTileType(self):
		if self.lineSensor.IsBlackTile():
			return TileType.Black
		else:
			return TileType.White

	"""
	### Motor Control ###
	"""

	def MotorSpeedCalibration(self, speed):
		mLeft = 0
		mRight = 0

		if speed == 1:
			mLeft = 20
			mRight = 18
		elif speed == 2:
			mLeft = 40
			mRight = 41
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


	def Left(self, speed = 4):
		(speedLeft, speedRight) = self.MotorSpeedCalibration(speed)
		self.MotorLeft.Backward(speedLeft)
		self.MotorRight.Forward(speedRight)


	def Right(self, speed = 4):
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
		self.Stop()