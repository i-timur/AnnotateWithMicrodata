import re

from html import unescape

def clear_string(string: str) -> str:
    """
    Clear string from HTML tags, new lines, tabs, multiple spaces and leading/trailing spaces.
    :param string:
    :return:
    """
    string = re.sub("<.*?>", "", str(string))
    string = unescape(string)
    string = re.sub(r"[\n\t\r]+", "", string)
    string = re.sub(r" +", " ", string)
    string = string.strip()
    return string
