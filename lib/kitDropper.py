import time
import RPi.GPIO as GPIO

class KitDropper():

    OpenPos = 9
    ClosePos = 3
    OpenTime = 0.5
    CloseTime = 0.25

    def __init__(self, pin):
        self.pin = pin
        
        GPIO.setup(self.pin, GPIO.OUT)
        self.Servo = GPIO.PWM(self.pin, 50)
        
        self.Servo.start(self.ClosePos)
        time.sleep(self.CloseTime)
        self.Servo.stop()

    def drop(self, ammount=1):
        
        self.Servo = GPIO.PWM(self.pin, 50)

        self.Servo.start(self.ClosePos)
        
        for x in range(0, ammount):
            
            self.Servo.ChangeDutyCycle(self.OpenPos)
            time.sleep(self.OpenTime)

            self.Servo.ChangeDutyCycle(self.ClosePos)
            time.sleep(self.CloseTime)

        self.Servo.stop()
