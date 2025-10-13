from gpiozero import Servo
import time

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
