#Image Processing
import numpy as np
import imutils
import cv2
import time
import picamera
import picamera.array

class Camera():

    def __init__(self, width =  640, height = 480):
        self.camera = picamera.PiCamera()
        self.camera.resolution = (width, height)

    def GetImage(self):
        stream = picamera.array.PiRGBArray(self.camera)
        self.camera.capture(stream, 'bgr', use_video_port=True)
        # stream.array now contains the image data in BGR order
        frame = stream.array
        
        cv2.imshow('Output', frame)

        key = cv2.waitKey(0) & 0xFF
            
        # reset the stream before the next capture
        stream.seek(0)
        stream.truncate()
        
        cv2.destroyAllWindows()