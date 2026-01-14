#from picamera2 import Picamera2
#from libcamera import Transform
import cv2
import time

def take_picture(path):
    """
    This function simply takes a photo with the raspi's webcam.
    """

    try:
        # Initialize camera
        #cam = Picamera2()
        #cam.configure(cam.create_still_configuration(transform=Transform(hflip=True, vflip=False)))
        cam = cv2.VideoCapture(0, cv2.CAP_V4L2)

        # Take photo
        #cam.start()
        time.sleep(1)
        ok, frame = cam.read()
        #cam.capture_file(path)
        #cam.stop()

        if ok:
            frame = cv2.flip(frame, 1)
            cv2.imwrite(path, frame)
        
        # Reset
        #cam.close()
        cam.release()
        cam = None
            
    except Exception as e:
        print("Camera error:", e)

def main():
    take_picture('/home/colecodes/projects/Pico/images/photo.jpg')

if __name__ == '__main__':
    main()