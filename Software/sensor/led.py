import time
import RPi.GPIO as GPIO

class LED():

	BlinkTime = 0.2

	def __init__(self, pin):
		self.pin = pin
		
		GPIO.setup(self.pin, GPIO.OUT)

	def TurnOn(self):
		GPIO.output(self.pin, True)

	def TurnOff(self):
		GPIO.output(self.pin, False)

	def Blink(self, repeat = 10):
		for i in range(repeat):
			GPIO.output(self.pin, True)
			time.sleep(self.BlinkTime)
			GPIO.output(self.pin, False)