"""
    Validators module, tools to validate some cases.
"""
import re

def validate_letters_only(value: str) -> bool:
    """This function validate if the value contain olny letters

    Args:
        value (str): text to be validated

    Returns:
        bool: True if the value contains olny letters and false otherwise.
    """
    regex = r'^[a-zA-Z\s]+$'
    return bool(re.match(regex, value))


def validate_letters_and_number(value: str) -> bool:
    """This function validate if the value contain letters and numbers

    Args:
        value (str): text to be validated

    Returns:
        bool: True if the value contains letters and numbers and false otherwise.
    """
    regex = r'^(?=.*[0-9])(?=.*[a-zA-Z])([a-zA-Z0-9]+)$'
    return bool(re.match(regex, value))
