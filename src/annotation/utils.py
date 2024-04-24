import re

def is_duration(text):
    pattern = r"^\d{1,3}\s?(m|min|minute|ms|mins|minutes)$|\d{1}\s?(h|hour|hs|hours)(\s\d{1,2}\s?(m|min|minute|ms|mins|minutes))?$"
    return bool(re.match(pattern, text))

def is_price(text):
    price_pattern = r'(\$|€|£|₽|¥|₹|₩|₴|₸|฿|₱|₪|₺|﷼|₡|₢|₫|₯|₠|₣|₤|₧|₦|₨|₮|₰|₲|₳|₭|₵|៛)\s?\d+(\.\d{1,2})?|\d+(\.\d{1,2})?\s?(\$|€|£|₽|¥|₹|₩|₴|₸|฿|₱|₪|₺|﷼|₡|₢|₫|₯|₠|₣|₤|₧|₦|₨|₮|₰|₲|₳|₭|₵|៛)'

    # Проверка на соответствие паттерну
    match = re.search(price_pattern, text)

    if match:
        return True
    else:
        return False

def is_discount(text):
    discount_pattern = r'\d{1,3}\s?%'

    match = re.search(discount_pattern, text)

    if match:
        return True
    else:
        return False
