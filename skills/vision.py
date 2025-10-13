from picamera2 import Picamera2
from time import sleep

def take_picture(path):
    # initialize camera
    try:
        cam = Picamera2()
        cam.configure(cam.create_still_configuration())

        # take photo
        cam.start()
        sleep(1)
        cam.capture_file(path)
        cam.stop()
        
        # reset cam so it can take another photo
        cam.close()
        cam = None
    except Exception as e:
        print("Camera module not connected:", e)