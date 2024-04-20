import re

def check_duration(text):
    pattern = r"^\d{1,3}\s?(m|min|minute|ms|mins|minutes)$|\d{1}\s?(h|hour|hs|hours)(\s\d{1,2}\s?(m|min|minute|ms|mins|minutes))?$"
    return bool(re.match(pattern, text))
