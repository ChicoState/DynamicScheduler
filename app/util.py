"""
A file containing utility functions
"""
# from jinja2 import Environment
from datetime import datetime, timedelta
# env = Environment()

def time_from_string(time: str):
    """
    Get time from string
    """
    # actually parse, this is just a placeholder
    if time == "1pm":
        return 780
    if time == "2pm":
        return 840
    return int(time)

def string_from_time(time: int):
    """
    Get string from time
    """
    # actually parse, this is just a placeholder
    hour = time / 60
    if hour == 0:
        hour = 12
    elif hour > 13:
        return f"{str(hour-12)}pm"
    signiture = ""
    if hour < 13:
        signiture = "am"
    else:
        signiture = "pm"

    minute = time % 60

    if minute == 0:
        return f"{hour}{signiture}"
    return f"{hour}{minute}{signiture}"


# Convert `from_time` and `to_time` to minutes since midnight
def time_to_minutes(t):
    """
    Convert time to minutes
    """
    hours, minutes = map(int, t.split(":"))
    return hours * 60 + minutes


def get_current_time_12h():
    """
    Get the current time in 12h format
    """
    now = datetime.now()
    pst_now = now - timedelta(hours=8)  # Convert to PST (8 hours behind UTC)
    return pst_now.strftime("%-I:%M %p")  # 12-hour format with AM/PM

def get_current_time_military():
    """
    Get current time in millitary time
    """
    now = datetime.now()
    pst_now = now - timedelta(hours=8)  # Convert to PST (8 hours behind UTC)
    return pst_now.strftime("%H:%M")  # 24-hour format without AM/PM

def get_current_time_mfm():
    """
    Get current time in minutes from midnight
    """
    now = get_current_time_military()
    now_mfm = time_to_minutes(now)
    return now_mfm # integer representing minutes from midnight

def get_current_date():
    """
    Get the current date
    """
    now = datetime.now()
    pst_now = now - timedelta(hours=8)  # Convert to PST (8 hours behind UTC)
    return pst_now.strftime("%d/%m/%Y")  # Day/Month/Year format

# env.globals['string_from_time'] = string_from_time
