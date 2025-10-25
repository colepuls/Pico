from gpiozero import Servo
import os

os.chdir("/home/colecodes/projects/Pico/motor_files") # make auto .lgd files stored in specific folder

# ----- Code for testing servo functionality -----
def attach_motor():
    motor = None
    pin = 21
    motor = Servo(pin)
    return motor

def run_motor_forward(motor):
    motor.value = 0.5

def run_motor_backward(motor):
    motor.value = -0.5

def stop_motor(motor):
    motor.detach()
    motor = None
        
