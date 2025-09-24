from gpiozero import Servo

servo = None
pin = 21

while True:
    press = input("g-run or s-stop: ")
    if press == "g":
        servo = Servo(pin)
        servo.value = 1
    elif press == "s":
        if servo:
            servo.detach()
            servo = None