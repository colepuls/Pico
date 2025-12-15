from gpiozero import AngularServo
import time
import os

os.chdir("/home/colecodes/projects/Pico/motor_files") # make auto .lgd files stored in specific folder

def dance():

    PIN = 21
            
    servo = AngularServo(PIN)

    for _ in range(3):
        servo.angle = 90
        time.sleep(1)
        servo.angle = -90
        time.sleep(1)

    servo.angle = 0
    time.sleep(1)
    servo.detach()