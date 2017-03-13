import time
import RPi.GPIO as GPIO

from lib.motor import Motor
from lib.srf04 import SRF04
#from lib.cmps03 import CMPS03
from lib.mlx90614 import MLX90614
from lib.hmc5883l import HMC5883L
from lib.kitDropper import KitDropper

class Robot():

    #Kit Dropper
    KitDropperPin = 7

    #MLX90614
    LeftThermometerAddr = 0x5a
    RightThermometerAddr = 0x2a

    #SRF04
    LeftSonarTRIG = 36
    LeftSonarECHO = 15
    
    FrontSonarTRIG = 38
    FrontSonarECHO = 23
    
    RightSonarTRIG = 40
    RightSonarECHO = 37

    #Pin1, Pin2
    Motor1 = [13, 11] #Motor in Top-Left
    Motor2 = [29, 31] #Motor in Top-Right
    Motor3 = [19, 21] #Motor in Bottom-Left
    Motor4 = [35, 33] #Motor in Bottom-Left

    #Vars
    tileSize = 30.0
    robotLenght = 21.0
    robotWidth = 13.0

    def __init__(self):
        
        GPIO.setmode(GPIO.BOARD)
        #GPIO.setwarnings(False)

        #Kit Dropper Setup
        self.kitDropper = KitDropper(self.KitDropperPin)

        #Gyroscope Setup
        self.gyroscope = HMC5883L()

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



    def GetSonar(self):
        leftCM = self.sonarLeft.getCM()

        frontCM = self.sonarFront.getCM()
        
        rightCM = self.sonarRight.getCM()

        return (leftCM, frontCM, rightCM)
        
        
    def GetTile(self, distance):
        tile = 0
        while distance >= self.tileSize:
            tile += 1
            distance -= self.tileSize

        exactPosition = False

        gap = (self.tileSize - self.robotLenght) / 2

        print gap

        if distance >= (gap - 0.5) and distance <= (gap + 0.5):
            exactPosition = True
        
        return (tile, exactPosition)

    def DropKit(self, ammount = 1):
        self.Break()
        
        time.sleep(0.1)

        self.kitDropper.drop(ammount)

    def GetXYZ(self):
        return self.gyroscope.GetXYZ()

    def IsVictim(self):
    
        self.ambTempLeft = self.thermometerLeft.get_amb_temp()
        self.objTempLeft = self.thermometerLeft.get_obj_temp()

        self.ambTempRight = self.thermometerRight.get_amb_temp()
        self.objTempRight = self.thermometerRight.get_obj_temp()
        
        print "Ambient Temperature Left : ", self.ambTempLeft
        print "Object Temperature Left : ", self.objTempLeft

        print "Ambient Temperature Right : ", self.ambTempRight
        print "Object Temperature Left : ", self.objTempRight

        if (self.objTempLeft - self.ambTempLeft) > 5 or (self.objTempRight - self.ambTempRight) > 5:
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

    def Exit(self):
        GPIO.cleanup()
