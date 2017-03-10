import time
import RPi.GPIO as GPIO

from lib.motor import Motor
from lib.srf04 import SRF04
from lib.cmps03 import CMPS03
from lib.mlx90614 import MLX90614
from lib.kitDropper import KitDropper

class Robot():

    #Kit Dropper
    KitDropperPin = 12

    #CMPS03
    CompassAddr = 0x60

    #MLX90614
    LeftThermometerAddr = 0x5a
    RightThermometerAddr = 0x2a

    #SRF04
    LeftSonarTRIG = 38
    LeftSonarECHO = 40
    
    FrontSonarTRIG = 38
    FrontSonarECHO = 40
    
    RightSonarTRIG = 38
    RightSonarECHO = 40

    #Pin1, Pin2
    Motor1 = [11, 13] #Motor in Top-Left
    Motor2 = [21, 19] #Motor in Top-Right
    Motor3 = [29, 31] #Motor in Bottom-Left
    Motor4 = [35, 37] #Motor in Bottom-Left

    def __init__(self):
        
        GPIO.setmode(GPIO.BOARD)
        #GPIO.setwarnings(False)

        #Kit Dropper Setup
        self.kitDropper = KitDropper(self.KitDropperPin)

        #Compass Setup
        self.compass = CMPS03(self.CompassAddr)

        #Thermometer Setup
        self.thermometerLeft = MLX90614(self.LeftThermometerAddr)
        self.thermometerRight = MLX90614(self.RightThermometerAddr)

        #Sonar Setup
        self.sonarLeft = SRF04(self.LeftSonarTRIG, self.LeftSonarECHO)
        self.sonarFront = SRF04(self.FrontSonarTRIG, self.FrontSonarECHO)
        self.sonarRight = SRF04(self.RightSonarTRIG, self.RightSonarECHO)

        #Motors Setup
        self.motor1 = Motor(self.Motor1[0], self.Motor1[1])
        self.motor2 = Motor(self.Motor2[0], self.Motor2[1])
        self.motor3 = Motor(self.Motor3[0], self.Motor3[1])
        self.motor4 = Motor(self.Motor4[0], self.Motor4[1])

        
    def GetDirection(self):
        self.direction = compass.bearing3599()
        return self.direction

    def GetSonar(self):   
        self.leftCM = self.sonarLeft.getCM()
        self.frontCM = self.sonarLeft.getCM()
        self.rightCM = self.sonarFront.getCM()

    def DropKit(self, ammount = 1):
        Break()
        
        time.sleep(1)

        self.kitDropper.drop(ammount)

    def IsVictim(self):
    
        ambTempLeft = 5#self.thermometerLeft.get_amb_temp()
        objTempLeft = 5#self.thermometerLeft.get_obj_temp()

        ambTempRight = self.thermometerRight.get_amb_temp()
        objTempRight = self.thermometerRight.get_obj_temp()

        if (objTempLeft - ambTempLeft) > 5 or (objTempRight - ambTempRight) > 5:
            return True
        else:
            return False


    def Forward(self):
        self.motor1.Forward()
        self.motor2.Forward()
        self.motor3.Forward()
        self.motor4.Forward()

    def Backward(self):
        self.motor1.Backward()
        self.motor2.Backward()
        self.motor3.Backward()
        self.motor4.Backward()


    def Left(self):
        self.motor1.Backward()
        self.motor2.Forward()
        self.motor3.Backward()
        self.motor4.Forward()


    def Right(self):
        self.motor1.Forward()
        self.motor2.Backward()
        self.motor3.Forward()
        self.motor4.Backward()


    def Stop(self):
        self.motor1.Stop()
        self.motor2.Stop()
        self.motor3.Stop()
        self.motor4.Stop()

    def Break(self):
        self.motor1.Break()
        self.motor2.Break()
        self.motor3.Break()
        self.motor4.Break()
