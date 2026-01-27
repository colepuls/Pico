from servo_control.bridge import send_angle
import time

def run_dance():
    for _ in range(3):
        send_angle(180)
        time.sleep(0.5)
        send_angle(0)
        time.sleep(0.5)
    send_angle(90)