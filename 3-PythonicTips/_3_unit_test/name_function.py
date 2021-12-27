# -*- coding: UTF-8 -*-
"""
@Project : 3-PythonicTips 
@File    : name_function.py
@IDE     : PyCharm 
@Author  : Peter
@Date    : 27/12/2021 02:42 
@Brief   : 
"""


def get_formatted_name(first: str, last: str, middle: str = '') -> str:
    """Generate a neatly formatter full name."""
    if middle:
        full_name = f"{first} {middle} {last}"
    else:
        full_name = f"{first} {last}"

    return full_name.title()


