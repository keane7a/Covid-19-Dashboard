from datetime import *

def minutes_to_seconds(minutes):
    """Converts minutes to seconds"""
    return int(minutes)*60

def hours_to_minutes(hours):
    """Converts hours to minutes"""
    return int(hours)*60

def hhmm_to_seconds(hhmm):
    if len(hhmm.split(':')) != 2:
        print('Incorrect format. Argument must be formatted as HH:MM' + hhmm)
        return None
    return minutes_to_seconds(hours_to_minutes(hhmm.split(':')[0])) + \
          minutes_to_seconds(hhmm.split(':')[1])

def time_difference_in_seconds(scheduled_time):
    """This function returns time difference of current time and scheduled time in seconds. 
    Note: uses 24 hour format!"""
    current_time = datetime.now().strftime("%H:%M")
    new_scheduled_time = int(hhmm_to_seconds(scheduled_time))
    new_current_time = int(hhmm_to_seconds(current_time))
    time_diffrence =  new_scheduled_time-new_current_time
    if time_diffrence >=0: 
        return int(time_diffrence)
    else: 
        return int(time_diffrence+86400)
    
