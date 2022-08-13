import datetime

from django.core.validators import MaxValueValidator


def max_value_current_year(value):
    return MaxValueValidator(
        datetime.date.today().year, "Год не может быть больше текущего")(
        value)
