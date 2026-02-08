from datetime import time
from django import forms

from .models import Booking


class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ["name", "email", "phone", "guests", "date", "time"]
        widgets = {
            "name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Your full name",
                }
            ),
            "email": forms.EmailInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "you@example.com",
                }
            ),
            "phone": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "+353 ...",
                }
            ),
            "guests": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "min": 1,
                    "max": 20,
                }
            ),
            "date": forms.DateInput(
                attrs={
                    "class": "form-control",
                    "type": "date",
                }
            ),
            "time": forms.TimeInput(
                attrs={
                    "class": "form-control",
                    "type": "time",
                    "step": 900,
                }
            ),
        }

    def clean_time(self):
        t = self.cleaned_data.get("time")
        if not t:
            return t

        # Allowed booking windows:
        # Lunch: 12:00–15:00
        # Dinner: 17:00–22:00
        lunch_start = time(12, 0)
        lunch_end = time(15, 0)
        dinner_start = time(17, 0)
        dinner_end = time(22, 0)

        in_lunch = lunch_start <= t < lunch_end
        in_dinner = dinner_start <= t < dinner_end

        if not (in_lunch or in_dinner):
            raise forms.ValidationError(
                "Please choose a time within our opening hours: "
                "12:00–15:00 or 17:00–22:00."
            )
        return t
