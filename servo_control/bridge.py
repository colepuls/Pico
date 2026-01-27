import serial
import time

SERIAL_PORT = "/dev/ttyACM0"
BAUD = 115200

ser = None

def get_serial():
    global ser
    if ser is None:
        ser = serial.Serial(SERIAL_PORT, BAUD, timeout=1)
        time.sleep(2)
    return ser

def send_angle(angle: float):
    ser = get_serial()
    ser.write(f"{angle}\n".encode())
    ser.flush()