from datetime import datetime

def run_time():
    time = datetime.now()
    time = time.strftime("%I:%M %p")
    return f"The time is {time}"

def run_date():
    now = datetime.now()
    date = now.strftime("%m/%d * %a")
    return date