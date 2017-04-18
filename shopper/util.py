import datetime

def elapsedTime(t1, t2):
    elapsedTime = t2 - t1
    seconds = elapsedTime.total_seconds()
    days = int(seconds // 86400)
    hours = int(seconds // 3600)
    mins = int(seconds // 60)
    time = ""
    if days > 0:
        time = str(days) + "d"
    elif hours > 0:
        time = str(hours) + "h"
    elif mins > 0:
        time = str(mins) + "m"
    else:
        time = "Just Now"
    return time

if __name__ == '__main__':
    print("util.py is not executable")
