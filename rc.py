import time
import Tkinter as tk
import RPi.GPIO as GPIO

from lib.mlx90614 import MLX90614
from lib.cmps03 import CMPS03
from lib.srf04 import SRF04
from lib.kitDropper import KitDropper

#GPIO.setwarnings(False)

GPIO.setmode(GPIO.BOARD)

#I2C Adresses
LeftThermometerAddr = 0x5a
RightThermometerAddr = 0x2a

CompassAddr = 0x60


#Pins

#SRF04
LeftSonarTRIG = 38
LeftSonarECHO = 40


#In1, In2, Enable
PinMotor1 = [11, 13] #Motor in Top-Left
PinMotor2 = [21, 19] #Motor in Top-Right
PinMotor3 = [29, 31] #Motor in Bottom-Left
PinMotor4 = [35, 37] #Motor in Bottom-Left

Motors = [PinMotor1, PinMotor2, PinMotor3, PinMotor4]

#Setup


for PinMotor in Motors:
    for pinMotor in PinMotor:
        GPIO.setup(pinMotor, GPIO.OUT)

def Forward(delay):
    GPIO.output(Motors[0][0], True)
    GPIO.output(Motors[0][1], False)
    GPIO.output(Motors[1][0], True)
    GPIO.output(Motors[1][1], False)
    GPIO.output(Motors[2][0], True)
    GPIO.output(Motors[2][1], False)
    GPIO.output(Motors[3][0], True)
    GPIO.output(Motors[3][1], False)

    time.sleep(delay)

def Backward():
    GPIO.output(Motors[0][0], False)
    GPIO.output(Motors[0][1], True)
    GPIO.output(Motors[1][0], False)
    GPIO.output(Motors[1][1], True)
    GPIO.output(Motors[2][0], False)
    GPIO.output(Motors[2][1], True)
    GPIO.output(Motors[3][0], False)
    GPIO.output(Motors[3][1], True)


def Left():
    GPIO.output(Motors[0][0], False)
    GPIO.output(Motors[0][1], True)
    GPIO.output(Motors[1][0], True)
    GPIO.output(Motors[1][1], False)
    GPIO.output(Motors[2][0], False)
    GPIO.output(Motors[2][1], True)
    GPIO.output(Motors[3][0], True)
    GPIO.output(Motors[3][1], False)


def Right():
    GPIO.output(Motors[0][0], True)
    GPIO.output(Motors[0][1], False)
    GPIO.output(Motors[1][0], False)
    GPIO.output(Motors[1][1], True)
    GPIO.output(Motors[2][0], True)
    GPIO.output(Motors[2][1], False)
    GPIO.output(Motors[3][0], False)
    GPIO.output(Motors[3][1], True)


def Stop():
    for PinMotor in Motors:
        for pinMotor in PinMotor:
            GPIO.output(pinMotor, False)


def GetTemp():
    
    #tempLeft = MLX90614(LeftThermometerAddr)
    tempRight = MLX90614(RightThermometerAddr)
    
    #print "Left Side Ambient Temperature: ", tempLeft.get_amb_temp()
    print "Right Side Ambient Temperature: ", tempRight.get_amb_temp()
    #print "Left Side Object Temperature: ", tempLeft.get_obj_temp()
    print "Right Side Object Temperature: ", tempRight.get_obj_temp()

def GetDirection():
    compass = COMPS03(CompassAddr)

    print compass.bearing3599()

def GetSonar():   
    sonarLeft = srf04(LeftSonarTRIG, LeftSonarECHO)
    print sonarLeft.getCM()

def DropKit():
    kitDropper = KitDropper(12)
    kitDropper.drop(2)


def key_input(event):
    key_press = event.char
    
    if key_press.lower() == 'w':
        Forward(sleep_time)
    elif key_press.lower() == 's':
        Backward(sleep_time)
    elif key_press.lower() == 'a':
        Left(sleep_time)
    elif key_press.lower() == 'd':
        Right(sleep_time)
    elif key_press.lower() == ' ':
        DropKit()
    elif key_press.lower() == 't':
        GetTemp()
    elif key_press.lower() == 'y':
        GetDirection()
    elif key_press.lower() == 'u':
        GetSonar()
        
    time.sleep(0.030)

    Stop()


root = tk.Tk()
root.bind('<KeyPress>', key_input)
root.mainloop()


GPIO.cleanup()
