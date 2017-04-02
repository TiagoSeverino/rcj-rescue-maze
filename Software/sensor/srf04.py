import time
import RPi.GPIO as GPIO


class SRF04():

	def __init__(self, trig, echo):
		self.trig = trig
		self.echo = echo

		# Set pins as output and input
		GPIO.setup(self.trig, GPIO.OUT)  # Trigger
		GPIO.setup(self.echo, GPIO.IN)      # Echo

	def getCM(self):
		# This function measures a distance
		GPIO.output(self.trig, True)
		time.sleep(0.00001)
		GPIO.output(self.trig, False)
		start = time.time()

		while GPIO.input(self.echo)==0:
			start = time.time()

		while GPIO.input(self.echo)==1:
			stop = time.time()

		elapsed = stop-start
		distance = (elapsed * 34300)/2

		time.sleep(0.01)

		return distance