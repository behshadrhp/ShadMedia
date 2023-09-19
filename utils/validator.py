from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator


username_regex = RegexValidator(
        regex=r'^[a-zA-Z][a-zA-Z0-9]{5,30}$',
        message='Only English letters and numbers are allowed, and the numbers must be after the letters, and the allowed characters are between 6 and 30',
)
email_regex = RegexValidator(
    regex=r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$',
    message='Your email is not valid'
)
