import time
import RPi.GPIO as GPIO

class LineSensor():

    def __init__(self, Pin):
        self.Pin = Pin
        GPIO.setup(self.Pin,GPIO.IN)                   #Set pin as GPIO in

    def IsVoidTile(self):
        isVoidTile = False
        if GPIO.input(self.Pin)==1:
            isVoidTile = True
        return isVoidTile
