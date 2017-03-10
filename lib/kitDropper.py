import time
import RPi.GPIO as GPIO

class KitDropper():

    OpenPos = 9
    ClosePos = 3
    OpenTime = 0.5
    CloseTime = 0.25

    def __init__(self, pin):
        self.pin = pin

    def drop(self, ammount=1):
        GPIO.setup(self.pin, GPIO.OUT)

        Servo = GPIO.PWM(self.pin, 50)
        Servo.start(self.ClosePos)
        
        for x in range(0, ammount):
            
            Servo.ChangeDutyCycle(self.ClosePos)
            time.sleep(self.CloseTime)

            Servo.ChangeDutyCycle(self.OpenPos)
            time.sleep(self.OpenTime)

            Servo.ChangeDutyCycle(self.ClosePos)
            time.sleep(self.CloseTime)

        Servo.stop()
