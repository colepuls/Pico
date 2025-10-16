from gpiozero import Servo
import time
import os

os.chdir("/home/colecodes/projects/Pico/motor_files") # make auto .lgd files stored in specific folder

# ----- Code for testing servo functionality -----
servo = None

def run_motor():
    global servo
    pin = 21
    servo = Servo(pin)
    servo.value = 1

def stop_motor():
    global servo
    servo.detach()
    servo = None
