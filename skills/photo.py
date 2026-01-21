from picamera2 import Picamera2
from libcamera import Transform
from PIL import Image
import time

def take_picture(path):
    """
    This function simply takes a photo with the raspi's webcam.
    """

    try:
        # Initialize camera
        cam = Picamera2()
        cam.configure(cam.create_still_configuration(transform=Transform(hflip=True, vflip=False)))

        # Take photo
        cam.start()
        time.sleep(1)
        cam.capture_file(path)
        cam.stop()
        # Reset
        cam.close()
            
    except Exception as e:
        print("Camera error:", e)

def main():
    take_picture('/home/colecodes/projects/Pico/images/photo.jpg')

if __name__ == '__main__':
    main()