import time
import RPi.GPIO as GPIO

class SRF04():

    # Modified From http://www.raspberrypi-spy.co.uk/2012/12/ultrasonic-distance-measurement-using-python-part-1/

    def __init__(self, TRIG, ECHO):
        self.TRIG = TRIG
        self.ECHO = ECHO

        GPIO.setup(self.TRIG,GPIO.OUT)                  #Set pin as GPIO out
        GPIO.setup(self.ECHO,GPIO.IN)                   #Set pin as GPIO in


    def getCM(self):
        
        GPIO.output(self.TRIG, False)                   #Set TRIG as LOW

        time.sleep(0.0001)
        
        GPIO.output(self.TRIG, True)                    #Set TRIG as HIGH
        time.sleep(0.00001)                             #Delay of 0.00001 seconds
        GPIO.output(self.TRIG, False)                   #Set TRIG as LOW

        duration = time.time()

        while GPIO.input(self.ECHO)==0:                 #Check whether the ECHO is LOW
            pulse_start = time.time()                   #Saves the last known time of LOW pulse
            
        
        while GPIO.input(self.ECHO)==1:                 #Check whether the ECHO is HIGH
            pulse_end = time.time()                     #Saves the last known time of HIGH pulse
            
        pulse_duration = pulse_end - pulse_start        #Get pulse duration to a variable

        distance = pulse_duration * 17150               #Multiply pulse duration by 17150 to get distance
        distance = round(distance, 2)                   #Round to two decimal points
        return distance
