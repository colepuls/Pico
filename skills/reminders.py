from datetime import datetime
import time
import threading
import sys, fcntl, termios # for auto \n

def reminder(scheduled_time, message):
    while datetime.now() < scheduled_time:
        time.sleep(5)
    fcntl.ioctl(sys.stdin.fileno(), termios.TIOCSTI, '\n') # automatically press enter after execution to go back to chatbot


def set_reminder(year, month, day, hour, minute, message):
    scheduled_time = datetime(year, month, day, hour, minute)
    thread = threading.Thread(target=reminder, args=(scheduled_time, message), daemon=True) # run reminder in background 
    thread.start()
    print(f"Reminder set for {scheduled_time.strftime('%Y-%m-%d %H:%M')}\n")