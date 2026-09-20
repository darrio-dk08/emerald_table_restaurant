from datetime import datetime
from unittest.mock import patch
from zoneinfo import ZoneInfo

from django.contrib.auth import get_user_model
from django.test import Client, TestCase, override_settings
from django.urls import reverse

from .forms import BookingForm
from .models import Booking


@override_settings(
    SECURE_SSL_REDIRECT=False,
    STORAGES={
        "default": {
            "BACKEND": "django.core.files.storage.FileSystemStorage",
        },
        "staticfiles": {
            "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
        },
    },
)
class AccountAndTimeTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.password = "Local-test-only-482!"
        cls.user = get_user_model().objects.create_user(
            username="existing_customer", password=cls.password,
        )

    def booking_data(self, **changes):
        data = {
            "name": "Test Customer",
            "email": "test@example.com",
            "phone": "+353 871234567",
            "guests": 2,
            "date": "2030-06-01",
            "time": "13:30",
        }
        data.update(changes)
        return data

    def test_registration_creates_account_with_hashed_password(self):
        response = self.client.post(reverse("signup"), {
            "username": "new_customer",
            "password1": self.password,
            "password2": self.password,
        })
        self.assertRedirects(response, reverse("login"))
        user = get_user_model().objects.get(username="new_customer")
        self.assertTrue(user.check_password(self.password))
        self.assertNotEqual(user.password, self.password)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        self.assertNotIn("_auth_user_id", self.client.session)

    def test_invalid_registration_does_not_create_account(self):
        cases = [
            ("new_customer", self.password, "Different-password-942!"),
            ("new_customer", "123", "123"),
            ("existing_customer", self.password, self.password),
        ]
        for username, first, second in cases:
            with self.subTest(username=username, password_length=len(first)):
                response = self.client.post(reverse("signup"), {
                    "username": username,
                    "password1": first,
                    "password2": second,
                })
                self.assertEqual(response.status_code, 200)
                self.assertTrue(response.context["form"].errors)
                self.assertEqual(get_user_model().objects.count(), 1)
                self.assertNotIn("_auth_user_id", self.client.session)

    def test_login_and_post_logout(self):
        response = self.client.post(reverse("login"), {
            "username": self.user.username,
            "password": self.password,
        })
        self.assertRedirects(response, reverse("booking_list"))
        self.assertEqual(
            self.client.session["_auth_user_id"], str(self.user.pk)
        )
        self.assertEqual(
            self.client.get(reverse("logout")).status_code, 405
        )
        self.assertIn("_auth_user_id", self.client.session)
        self.assertRedirects(
            self.client.post(reverse("logout")), reverse("home")
        )
        self.assertNotIn("_auth_user_id", self.client.session)
        self.assertEqual(
            self.client.get(reverse("booking_list")).status_code, 302
        )

    def test_wrong_password_does_not_log_in(self):
        response = self.client.post(reverse("login"), {
            "username": self.user.username,
            "password": "Incorrect-password-991!",
        })
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context["form"].errors)
        self.assertNotIn("_auth_user_id", self.client.session)

    def test_login_checks_next_redirect(self):
        for target, expected in [
            (reverse("booking"), reverse("booking")),
            ("https://example.com/", reverse("booking_list")),
            ("//example.com/", reverse("booking_list")),
        ]:
            with self.subTest(target=target):
                self.client.logout()
                response = self.client.post(reverse("login"), {
                    "username": self.user.username,
                    "password": self.password,
                    "next": target,
                })
                self.assertRedirects(response, expected)

    def test_account_posts_require_csrf(self):
        client = Client(enforce_csrf_checks=True)
        for name in ["signup", "login"]:
            self.assertEqual(
                client.post(reverse(name), {}).status_code, 403
            )
        client.force_login(self.user)
        self.assertEqual(
            client.post(reverse("logout"), {}).status_code, 403
        )
        self.assertIn("_auth_user_id", client.session)
        self.assertEqual(get_user_model().objects.count(), 1)

    def test_same_day_elapsed_and_current_times_rejected(self):
        now = datetime(2030, 6, 1, 13, 15, tzinfo=ZoneInfo("Europe/Dublin"))
        self.client.force_login(self.user)
        booking = Booking.objects.create(
            owner=self.user, **self.booking_data()
        )
        urls = [
            reverse("booking"),
            reverse("edit_booking", args=[booking.pk]),
        ]
        with patch(
            "restaurant.validators.timezone.localtime", return_value=now
        ):
            for value in ["13:00", "13:15"]:
                for url in urls:
                    with self.subTest(time=value, url=url):
                        response = self.client.post(
                            url, self.booking_data(time=value)
                        )
                        self.assertEqual(response.status_code, 200)
                        self.assertIn("time", response.context["form"].errors)
                        self.assertEqual(Booking.objects.count(), 1)
                        booking.refresh_from_db()
                        self.assertEqual(str(booking.time), "13:30:00")

            response = self.client.post(
                reverse("booking"), self.booking_data(time="13:30")
            )
            self.assertRedirects(response, reverse("booking_success"))
            self.assertEqual(Booking.objects.count(), 2)

    def test_opening_and_closing_boundaries(self):
        now = datetime(2030, 6, 1, 10, 0, tzinfo=ZoneInfo("Europe/Dublin"))
        with patch(
            "restaurant.validators.timezone.localtime", return_value=now
        ):
            for value in ["12:00", "14:45", "17:00", "21:45"]:
                with self.subTest(accepted=value):
                    form = BookingForm(
                        self.booking_data(time=value),
                        instance=Booking(owner=self.user),
                    )
                    self.assertTrue(form.is_valid(), form.errors.as_text())

            for value in ["11:45", "15:00", "16:45", "22:00"]:
                with self.subTest(rejected=value):
                    form = BookingForm(
                        self.booking_data(time=value),
                        instance=Booking(owner=self.user),
                    )
                    self.assertFalse(form.is_valid())
                    self.assertIn("time", form.errors)
