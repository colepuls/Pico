from servo_control.bridge import send_angle
import time, random

def get_random_after_sound():
    after_sounds = [
        "I call that the servo shuffle.",
        "That cost extra battery.",
        "Did you see that?",
        "That voids my warranty.",
        "I trained years for that.",
    ]
    
    return random.choice(after_sounds)
    

def dance1():
    for _ in range(3):
        send_angle(180)
        time.sleep(0.3)
        send_angle(0)
        time.sleep(0.3)
    send_angle(90)


def dance2():
    for _ in range(10):
        send_angle(90)
        time.sleep(0.1)
        send_angle(0)
        time.sleep(0.1)
    send_angle(90)


def dance3():
    for _ in range(5):
        send_angle(90)
        time.sleep(0.1)
        send_angle(0)
        time.sleep(0.5)
        send_angle(180)
        time.sleep(0.3)
        send_angle(0)
        time.sleep(0.7)
    send_angle(90)


def run_dance():
    dances = [dance1, dance2, dance3]
    dance = random.choice(dances)
    dance()
    return get_random_after_sound()