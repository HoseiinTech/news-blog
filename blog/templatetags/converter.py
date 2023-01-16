from django import template

register = template.Library()

numbers = {
    "0": "۰",
    "1": "۱",
    "2": "۲",
    "3": "۳",
    "4": "۴",
    "5": "۵",
    "6": "۶",
    "7": "۷",
    "8": "۸",
    "9": "۹",
}


@register.filter
def translate_numbers(value):
    value = str(value)
    for e, p in numbers.items():
        value = value.replace(e, p)
    return value
