import re
from django.core.exceptions import ValidationError


def validate_email_username(value):
    """
    Email format validator

    :param value: string to evaluate
    """
    email_regex = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    if not re.match(email_regex, value):
        raise ValidationError("Username must be a valid email address.")
