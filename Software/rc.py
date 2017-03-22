import time
import Tkinter as tk
from robot import Robot

#Image Processing
import numpy as np
import imutils
import cv2
import time
import picamera
import picamera.array

greenLower = (10, 200, 150)
greenUpper = (20, 255, 185)

robot = Robot()
 
with picamera.PiCamera() as camera:
    with picamera.array.PiRGBArray(camera) as stream:
        camera.resolution = (208, 160)

        while True:
            camera.capture(stream, 'bgr', use_video_port=True)
            # stream.array now contains the image data in BGR order
            frame = stream.array
            
            cv2.imshow('Output', frame)

            key = cv2.waitKey(10) & 0xFF
            
            if key == ord('w'):
                robot.Forward()
            elif key == ord('s'):
                robot.Backward()
            elif key == ord('a'):
                robot.Left()
            elif key == ord('d'):
                robot.Right()
            elif key == ord(' '):
                robot.DropKit()
            elif key == ord('1'):
                robot.IsBlackTile()
            elif key == ord('2'):
                robot.GetLeftSonar()
            elif key == ord('3'):
                robot.GetFrontSonar()
            elif key == ord('4'):
                robot.GetRightSonar()
            elif key == ord('5'):
                robot.GetBearing()
            elif key == ord('6'):
                robot.GetPich()
            elif key == ord('7'):
                robot.GetRoll()
            elif key == ord('8'):
                robot.GetTemperatureLeft()
            elif key == ord('9'):
                robot.GetTemperatureRight()
			elif key == ord('q'):
                break
            else:
                robot.Stop()
                
            # reset the stream before the next capture
            stream.seek(0)
            stream.truncate()

        cv2.destroyAllWindows()
        robot.Exit()
        

