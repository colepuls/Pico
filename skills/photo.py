from picamera2 import Picamera2
from libcamera import Transform
import time
from PIL import Image

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

def convert_ascii(path):
    chars = " .:-=+*#%@"
    img = Image.open(path).convert("L").resize((80, 40))
    for i, p in enumerate(img.getdata()):
        print(chars[p * (len(chars)-1) // 255], end="\n" if (i+1) % 80 == 0 else "")

def main():
    # take_picture('/home/colecodes/projects/Pico/images/recent_photo.jpg')
    convert_ascii('/home/colecodes/projects/Pico/images/recent_photo.jpg')

if __name__ == '__main__':
    main()