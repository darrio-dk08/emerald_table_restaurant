"""Restaurant booking rules shared by customer and admin forms."""

from datetime import datetime, time

from django.core.exceptions import ValidationError
from django.utils import timezone


OPENING_WINDOWS = ((time(12), time(15)), (time(17), time(22)))


def validate_booking_datetime(booking_date, booking_time):
    errors = {}
    now = timezone.localtime()

    if booking_date and booking_date < now.date():
        errors["date"] = "Choose today or a future date."

    if booking_time:
        if not any(
            start <= booking_time < end
            for start, end in OPENING_WINDOWS
        ):
            errors["time"] = "Choose 12:00–14:45 or 17:00–21:45."
        elif (
            booking_time.minute % 15
            or booking_time.second
            or booking_time.microsecond
        ):
            errors["time"] = "Choose a 15-minute slot."

    if booking_date and booking_time and "date" not in errors:
        requested = timezone.make_aware(
            datetime.combine(booking_date, booking_time),
            timezone.get_current_timezone(),
        )

        if requested <= now:
            errors["time"] = "Choose a booking time in the future."

    if errors:
        raise ValidationError(errors)