import RPi.GPIO as GPIO
import time

class LineSensor():

	def __init__(self, Pin):
		self.Pin = Pin
		GPIO.setup(self.Pin,GPIO.IN)                   #Set pin as GPIO in

	def IsBlackTile(self):
		firstRead = GPIO.input(self.Pin)
		
		ReadSum = 0
		count = 50

		for i in range(count):
			ReadSum += GPIO.input(self.Pin)
			time.sleep(0.001)

		if firstRead * 50 == ReadSum:
			return True if firstRead == 1 else False
		else:
			return self.IsBlackTile()