from datetime import datetime

def get_current_time():
    time = datetime.now()
    time = time.strftime("%I:%M %p")
    return time