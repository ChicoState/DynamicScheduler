# from jinja2 import Environment

# env = Environment()

def time_from_string(time: str):
    # actually parse, this is just a placeholder
    if time == "1pm":
        return 780
    elif time == "2pm":
        return 840
    else:
        return int(time)
    
def string_from_time(time: int):
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
    hours, minutes = map(int, t.split(":"))
    return hours * 60 + minutes

### return a uri with specified fields; path required
def formatURI(path:str, **kwargs):
    """
    Return a uri with specified fields; path required

    **Example:** formatURI("/mypath", dayNum="10", monthNum="4") -> "/mypath?dayNum=10&monthNum=4"
    """
    if(len(kwargs) == 0):
        return path
    s = f"{path}?"
    for k, v in kwargs.items():
        s += f"{k}={v}&"
    return s[:-1] # drop last '&'

# env.globals['string_from_time'] = string_from_time