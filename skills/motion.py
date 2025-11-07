from gpiozero import Servo
import os

os.chdir("/home/colecodes/projects/Pico/motor_files") # make auto .lgd files stored in specific folder

def attach_motor():
    """
    This function attatches the motor to the rasppi.
    """
    motor = None
    pin = 21
    motor = Servo(pin)
    return motor

def run_motor_forward(motor):
    """
    Spins motor forward.
    """
    motor.value = 0.5

def run_motor_backward(motor):
    """
    Spins motor backward.
    """
    motor.value = -0.5

def stop_motor(motor):
    """
    Dettaches motor from rasppi.
    - Prevents motor jitter. 
    """
    motor.detach()
    motor = None
        
