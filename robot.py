import time
import RPi.GPIO as GPIO

from lib.motor import Motor
from lib.srf04 import SRF04
from lib.cmps10 import CMPS10
# from lib.cmps03 import CMPS03
from lib.mlx90614 import MLX90614
from lib.lineSensor import LineSensor
from lib.kitDropper import KitDropper

class Robot():

    #Kit Dropper
    KitDropperPin = 7

    #MLX90614
    LeftThermometerAddr = 0x5a
    RightThermometerAddr = 0x2a

    #Line Sensor
    LineSensorPin = 32

    #SRF04
    LeftSonarTRIG = 8
    LeftSonarECHO = 11
    
    FrontSonarTRIG = 10
    FrontSonarECHO = 13
    
    RightSonarTRIG = 12
    RightSonarECHO = 15

    #Pin1, Pin2
    motorLeft = [31, 33] #Motor in Left
    motorRight = [35, 37] #Motor in Right

    def __init__(self):
        
        GPIO.setmode(GPIO.BOARD)
        #GPIO.setwarnings(False)

        #Line Sensor Setup
        self.LineSensor = LineSensor(self.LineSensorPin)

        #Kit Dropper Setup
        self.kitDropper = KitDropper(self.KitDropperPin)

        #Compass Setup
        self.compass = CMPS10()

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
        print "Left Sonar: ", self.sonarLeft.raw_distance()
        print "Front Sonar: ", self.sonarFront.raw_distance()
        print "Right Sonar: ", self.sonarRight.raw_distance()

    def DropKit(self, ammount = 1):
        self.Break()
        time.sleep(0.1)
        self.kitDropper.drop(ammount)

    def GetXYZ(self):
        print "0-255: ", self.compass.bearing255()
        print "0-360.0: ", self.compass.bearing3599()
        print "Pich: ", self.compass.pich()
        print "Roll: ", self.compass.roll()

    def IsVictim(self):
    
        self.ambTempLeft = self.thermometerLeft.get_amb_temp()
        self.objTempLeft = self.thermometerLeft.get_obj_temp()

        self.ambTempRight = self.thermometerRight.get_amb_temp()
        self.objTempRight = self.thermometerRight.get_obj_temp()
        
        print "Ambient Temperature Left: ", self.ambTempLeft
        print "Object Temperature Left: ", self.objTempLeft

        print "Ambient Temperature Right: ", self.ambTempRight
        print "Object Temperature Right: ", self.objTempRight


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
