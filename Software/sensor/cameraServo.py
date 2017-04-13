import time
import RPi.GPIO as GPIO

class CameraServo():

    LeftPos = 12
    FrontPos = 7.5
    RightPos = 3    

    #Positions: 0 -> Left, 1-> Front, 2 -> Right
    LastPos = 1

    Time90Deg = 0.75

    def __init__(self, pin):
        self.pin = pin
        
        GPIO.setup(self.pin, GPIO.OUT)
        
        self.Rotate()

    def Rotate(self, position = 3):
        
        self.Servo = GPIO.PWM(self.pin, 50)
        self.Servo.start(self.FrontPos)

        sleepTime = self.Time90Deg

        if position == 3:
            self.Servo.ChangeDutyCycle(self.FrontPos)
            self.LastPos = 1
            sleepTime = self.Time90Deg * 2

        elif position == 0:
            self.Servo.ChangeDutyCycle(self.LeftPos)
            self.LastPos = 0

            if self.LastPos == 2:
                sleepTime = self.Time90Deg * 2

        elif position == 1:

            self.Servo.ChangeDutyCycle(self.FrontPos)
            self.LastPos = 1

        elif position == 2:

            self.Servo.ChangeDutyCycle(self.RightPos)
            self.LastPos = 2

            if self.LastPos == 0:
                sleepTime = self.Time90Deg * 2

        time.sleep(sleepTime)

        self.Servo.stop()
