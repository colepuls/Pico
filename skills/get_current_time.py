from datetime import datetime

def get_time():
    """
    This function simply gets the current time using the datatime library.
    """
    time = datetime.now()
    time = time.strftime("%I:%M %p")
    return f"The time is {time}"

def get_time_skill():
    time = datetime.now()
    time = time.strftime("%I:%M %p")
    return time

def get_date_skill():
    now = datetime.now()
    date = now.strftime("%m/%d * %a")
    return date

if __name__ == '__main__':
    date = get_date_skill()
    print(date)