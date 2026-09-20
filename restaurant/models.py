from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import (
    MaxValueValidator,
    MinValueValidator,
    RegexValidator,
)
from django.db import models

from .validators import validate_booking_datetime


class MenuItem(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return f"{self.name} - €{self.price}"


class Booking(models.Model):
    # NULL preserves legacy bookings without guessing their owners.
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="bookings",
    )
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(
        max_length=20,
        validators=[
            RegexValidator(
                regex=r"^\+?[0-9 ()-]{7,20}$",
                message=(
                    "Use digits, spaces, +, () or - for your phone number."
                ),
            )
        ],
    )
    guests = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(8)],
    )
    date = models.DateField()
    time = models.TimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    def clean(self):
        super().clean()

        if self._state.adding and self.owner_id is None:
            raise ValidationError("New bookings require an owner.")

        validate_booking_datetime(self.date, self.time)

    def __str__(self):
        return f"Booking for {self.name} on {self.date} at {self.time}"