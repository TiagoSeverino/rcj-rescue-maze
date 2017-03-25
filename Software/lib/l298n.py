import RPi.GPIO as GPIO

#Using 2 L149.4.90 Motors

class L298N():

	def __init__(self, pin1, pin2, pwm):
		self.pin1 = pin1
		self.pin2 = pin2
		self.pwm = pwm
		
		GPIO.setup(self.pin1, GPIO.OUT)
		GPIO.setup(self.pin2, GPIO.OUT)
		GPIO.setup(self.pwm, GPIO.OUT)

		self.PWM = GPIO.PWM(self.pwm, 50)

		self.lastPWM = 0

		self.PWM.start(self.lastPWM)

	def Forward(self, dc = 100):
		GPIO.output(self.pin1, True)
		GPIO.output(self.pin2, False)

		if dc != self.lastPWM:
			self.PWM.ChangeDutyCycle(dc)
			self.lastPWM = dc

	def Backward(self, dc = 100):
		GPIO.output(self.pin1, False)
		GPIO.output(self.pin2, True)

		if dc != self.lastPWM:
			self.PWM.ChangeDutyCycle(dc)
			self.lastPWM = dc

	def Stop(self, dc = 0):
		GPIO.output(self.pin1, False)
		GPIO.output(self.pin2, False)

		if dc != self.lastPWM:
			self.PWM.ChangeDutyCycle(dc)
			self.lastPWM = dc

	def Break(self, dc = 100):
		GPIO.output(self.pin1, True)
		GPIO.output(self.pin2, True)

		if dc != self.lastPWM:
			self.PWM.ChangeDutyCycle(dc)
			self.lastPWM = dc