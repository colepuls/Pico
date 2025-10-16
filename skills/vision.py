from picamera2 import Picamera2
from time import sleep

# ----- Code for testing camera -----
def take_picture(path):
    # Initialize camera
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