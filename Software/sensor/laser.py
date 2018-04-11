import time
import VL53L0X
import RPi.GPIO as GPIO

class Lasers():
    lateral_range_mode = VL53L0X.VL53L0X_GOOD_ACCURACY_MODE
    front_range_mode = VL53L0X.VL53L0X_LONG_RANGE_MODE

    timing = []

    def __init__(self, Xshut1, Xshut2, Xshut3, Xshut4, Xshut5):
        GPIO.setmode(GPIO.BOARD)

        self.XShut = []

        self.XShut.append(Xshut1)
        self.XShut.append(Xshut2)
        self.XShut.append(Xshut3)
        self.XShut.append(Xshut4)
        self.XShut.append(Xshut5)

        self.setup()

    def setup(self):
        # Set pins as output
        for XShut in self.XShut:
            GPIO.setup(XShut, GPIO.OUT)
            GPIO.output(XShut, GPIO.LOW)
        time.sleep(0.10)

        self.tof = []
        self.tof.append(VL53L0X.VL53L0X(address=0x2B))
        self.tof.append(VL53L0X.VL53L0X(address=0x2D))
        self.tof.append(VL53L0X.VL53L0X(address=0x2F))
        self.tof.append(VL53L0X .VL53L0X(address=0x30))
        self.tof.append(VL53L0X.VL53L0X(address=0x32))

        for index, tof in enumerate(self.tof):
            print self.XShut[index]
            GPIO.output(self.XShut[index], GPIO.HIGH)
            time.sleep(0.50)
            self.tof[index].start_ranging(self.front_range_mode if (index == Laser.Front) else self.lateral_range_mode)
 
            self.timing[index] = tof[index].get_timing()
            if (self.timing[index] < 20000):
                self.timing[index] = 20000
            print ("Laser Timing %d ms" % (self.timing[index]/1000))

    def getCM(self, laserID):
        distance = self.tof[laserID].get_distance()/10.00
        time.sleep(self.timing[laserID]/1000000.00/2.00)
        return distance

class Laser:
    FrontLeft = 0
    Front = 1
    FrontRight = 2
    BackRight = 3
    BackLeft = 4
