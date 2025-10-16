from datetime import datetime

# ----- Funnction for getting the current time -----
def get_time():
    time = datetime.now()
    time = time.strftime("%I:%M %p")
    return time