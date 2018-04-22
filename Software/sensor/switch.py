import time
import RPi.GPIO as GPIO

class SWITCH():

	def __init__(self, pin):
		self.pin = pin
		
		GPIO.setup(self.pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

	def IsOn(self):
		firstRead = GPIO.input(self.pin)
		
		ReadSum = 0
		count = 5

		for i in range(count):
			ReadSum += GPIO.input(self.pin)
			time.sleep(0.0001)

		if firstRead * count == ReadSum:
			return True if firstRead == 1 else False
		else:
			return self.IsOn()