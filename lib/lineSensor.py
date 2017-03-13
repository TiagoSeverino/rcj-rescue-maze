import time
import RPi.GPIO as GPIO

class LineSensor():

    # Modified From http://www.raspberrypi-spy.co.uk/2012/12/ultrasonic-distance-measurement-using-python-part-1/

    def __init__(self, Pin):
        self.Pin = Pin
        GPIO.setup(self.Pin,GPIO.IN)                   #Set pin as GPIO in


    def IsVoidTile(self):
        isVoidTile = False
        if GPIO.input(self.Pin)==1:
            isVoidTile = True
        return isVoidTile
