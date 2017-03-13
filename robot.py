import time
import RPi.GPIO as GPIO

from lib.motor import Motor
from lib.srf04 import SRF04
#from lib.cmps03 import CMPS03
from lib.mlx90614 import MLX90614
from lib.hmc5883l import HMC5883L
from lib.lineSensor import LineSensor
from lib.kitDropper import KitDropper

class Robot():

    #Kit Dropper
    KitDropperPin = 7

    #MLX90614
    LeftThermometerAddr = 0x5a
    RightThermometerAddr = 0x2a

    #Line Sensor
    LineSensorPin = 26

    #SRF04
    LeftSonarTRIG = 36
    LeftSonarECHO = 15
    
    FrontSonarTRIG = 38
    FrontSonarECHO = 23
    
    RightSonarTRIG = 40
    RightSonarECHO = 32

    #Pin1, Pin2
    motorLeft = [37, 35] #Motor in Left
    motorRight = [33, 31] #Motor in Right

    #Vars
    tileSize = 30.0
    robotLenght = 21.0
    robotWidth = 13.0

    def __init__(self):
        
        GPIO.setmode(GPIO.BOARD)
        #GPIO.setwarnings(False)

        #Line Sensor Setup
        self.LineSensor = LineSensor(self.LineSensorPin)

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
        self.MotorLeft = Motor(self.motorLeft[0], self.motorLeft[1])
        self.MotorRight = Motor(self.motorRight[0], self.motorRight[1])

    def IsVoidTile(self):
        print self.LineSensor.IsVoidTile()


    def GetSonar(self):
        leftCM = self.sonarLeft.getCM()

        frontCM = self.sonarFront.getCM()
        
        rightCM = self.sonarRight.getCM()

        print leftCM, frontCM, rightCM

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
        self.MotorLeft.Forward()
        self.MotorRight.Forward()

    def Backward(self):
        self.MotorLeft.Backward()
        self.MotorRight.Backward()


    def Left(self):
        self.MotorLeft.Backward()
        self.MotorRight.Forward()

    def Right(self):
        self.MotorLeft.Forward()
        self.MotorRight.Backward()


    def Stop(self):
        self.MotorLeft.Stop()
        self.MotorRight.Stop()

    def Break(self):
        self.MotorLeft.Break()
        self.MotorRight.Break()

    def Exit(self):
        GPIO.cleanup()
