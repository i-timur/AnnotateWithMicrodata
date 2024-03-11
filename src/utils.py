import re

from html import unescape

CLASS_MAP = {
    0: "https://schema.org/Product",
    1: "https://schema.org/Book",
    2: "https://schema.org/Event",
    3: "https://schema.org/Hotel",
    4: "https://schema.org/JobPosting",
    5: "https://schema.org/Movie",
    6: "https://schema.org/Recipe",
    7: "https://schema.org/Restaurant"
}

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
