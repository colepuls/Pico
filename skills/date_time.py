from datetime import datetime

# current time
def run_time():
    time = datetime.now()
    time = time.strftime("%I:%M %p")
    return f"The time is {time}"

# todays date
def run_date():
    now = datetime.now()
    date = now.strftime("%m/%d * %a")
    return f"The date is {date}"