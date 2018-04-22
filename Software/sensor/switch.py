import time
import RPi.GPIO as GPIO

class SWITCH():

	def __init__(self, pin):
		self.pin = pin
		
		GPIO.setup(self.pin, GPIO.IN)

	def IsOn(self):
		firstRead = GPIO.input(self.pin)
		
		ReadSum = 0
		count = 10

		for i in range(count):
			ReadSum += GPIO.input(self.pin)
			time.sleep(0.0001)

		if firstRead * 5 == ReadSum:
			return True if firstRead == 1 else False
		else:
			return self.IsOn()