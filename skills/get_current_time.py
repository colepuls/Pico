from datetime import datetime

def get_time():
    """
    This function simply gets the current time using the datatime library.
    """
    time = datetime.now()
    time = time.strftime("%I:%M %p")
    return time