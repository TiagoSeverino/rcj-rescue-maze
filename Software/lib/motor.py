import RPi.GPIO as GPIO

class Motor():

	def __init__(self, pin1, pin2):
		self.pin1 = pin1
		self.pin2 = pin2
		
		GPIO.setup(self.pin1, GPIO.OUT)
		GPIO.setup(self.pin2, GPIO.OUT)

	def Forward(self):
		GPIO.output(self.pin1, True)
		GPIO.output(self.pin2, False)

	def Backward(self):
		GPIO.output(self.pin1, False)
		GPIO.output(self.pin2, True)

	def Stop(self):
		GPIO.output(self.pin1, False)
		GPIO.output(self.pin2, False)

	def Break(self):
		GPIO.output(self.pin1, True)
		GPIO.output(self.pin2, True)
