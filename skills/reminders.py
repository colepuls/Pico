from datetime import datetime
import time
import threading

def reminder(scheduled_time, message):
    while datetime.now() < scheduled_time:
        time.sleep(10)
    print(f"\n[Reminder] {message}\n")

def set_reminder(year, month, day, hour, minute, message):
    scheduled_time = datetime(year, month, day, hour, minute)
    thread = threading.Thread(target=reminder, args=(scheduled_time, message)) # run reminder in background 
    daemon = True
    thread.start()
    print(f"Reminder set for {scheduled_time.strftime('%Y-%m-%d %H:%M')}")

#def main():
#    t = set_reminder(2025, 10, 13, 22, 3, "Baka")
#    print("Main running...\n")
#    t.join()