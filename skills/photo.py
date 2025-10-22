from picamera2 import Picamera2
from libcamera import Transform
import time

# ----- Code to take a photo -----
def take_picture(path):
    try:
        # Initialize camera
        cam = Picamera2()
        cam.configure(cam.create_still_configuration(transform=Transform(hflip=True, vflip=True)))

        # take photo
        cam.start()
        time.sleep(1)
        cam.capture_file(path)
        cam.stop()
        
        # reset cam so it can take another photo
        cam.close()
        cam = None    
    except Exception as e:
        print("Camera error:", e)