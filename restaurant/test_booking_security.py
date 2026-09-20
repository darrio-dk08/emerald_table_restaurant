from datetime import timedelta

from django.contrib.auth import get_user_model
from django.test import Client, TestCase, override_settings
from django.urls import reverse
from django.utils import timezone

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
class BookingSecurityTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        User = get_user_model()
        cls.owner = User.objects.create_user(username="test_owner")
        cls.other = User.objects.create_user(username="test_other")

    def setUp(self):
        self.data = {
            "name": "Test Customer",
            "email": "customer@example.com",
            "phone": "+353 871234567",
            "guests": 2,
            "date": (timezone.localdate() + timedelta(days=3)).isoformat(),
            "time": "12:00",
        }
        self.booking = Booking.objects.create(
            owner=self.owner, **self.data
        )
        self.edit_url = reverse("edit_booking", args=[self.booking.pk])
        self.delete_url = reverse("delete_booking", args=[self.booking.pk])
        self.client.force_login(self.owner)

    def test_create_eight_guests_assigns_signed_in_owner(self):
        response = self.client.post(
            reverse("booking"),
            dict(self.data, guests=8, owner=self.other.pk),
        )
        self.assertRedirects(response, reverse("booking_success"))
        self.assertEqual(Booking.objects.count(), 2)
        created = Booking.objects.latest("pk")
        self.assertEqual(created.guests, 8)
        self.assertEqual(created.owner_id, self.owner.pk)

    def test_invalid_guest_counts_rejected_on_create_and_edit(self):
        for guests in [0, -1, 9, 20]:
            for url in [reverse("booking"), self.edit_url]:
                with self.subTest(guests=guests, url=url):
                    response = self.client.post(
                        url, dict(self.data, guests=guests)
                    )
                    self.assertEqual(response.status_code, 200)
                    self.assertIn("guests", response.context["form"].errors)
                    self.assertEqual(Booking.objects.count(), 1)
                    self.booking.refresh_from_db()
                    self.assertEqual(self.booking.guests, 2)

    def test_past_date_rejected_on_create_and_edit(self):
        yesterday = (timezone.localdate() - timedelta(days=1)).isoformat()
        for url in [reverse("booking"), self.edit_url]:
            with self.subTest(url=url):
                response = self.client.post(
                    url, dict(self.data, date=yesterday)
                )
                self.assertEqual(response.status_code, 200)
                self.assertIn("date", response.context["form"].errors)
                self.assertEqual(Booking.objects.count(), 1)
                self.booking.refresh_from_db()
                self.assertEqual(str(self.booking.date), self.data["date"])

    def test_invalid_times_rejected_on_create_and_edit(self):
        for value in ["11:45", "15:00", "16:00", "22:00", "12:07"]:
            for url in [reverse("booking"), self.edit_url]:
                with self.subTest(time=value, url=url):
                    response = self.client.post(
                        url, dict(self.data, time=value)
                    )
                    self.assertEqual(response.status_code, 200)
                    self.assertIn("time", response.context["form"].errors)
                    self.assertEqual(Booking.objects.count(), 1)
                    self.booking.refresh_from_db()
                    self.assertEqual(str(self.booking.time), "12:00:00")

    def test_owner_can_update_to_eight_guests(self):
        response = self.client.post(
            self.edit_url,
            dict(self.data, guests=8, owner=self.other.pk),
            follow=True,
        )
        self.assertContains(response, "Booking updated.")
        self.booking.refresh_from_db()
        self.assertEqual(self.booking.guests, 8)
        self.assertEqual(self.booking.owner_id, self.owner.pk)

    def test_unchanged_edit_shows_honest_message(self):
        response = self.client.post(self.edit_url, self.data, follow=True)
        self.assertContains(response, "No changes were made to your booking.")
        self.assertNotContains(response, "Booking updated.")
        self.assertEqual(Booking.objects.count(), 1)

    def test_other_user_cannot_view_or_modify_booking(self):
        self.client.force_login(self.other)
        response = self.client.get(reverse("booking_list"))
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, self.data["email"])
        self.assertEqual(list(response.context["bookings"]), [])

        for url in [self.edit_url, self.delete_url]:
            with self.subTest(url=url):
                self.assertEqual(self.client.get(url).status_code, 404)
                response = self.client.post(
                    url, dict(self.data, guests=8)
                )
                self.assertEqual(response.status_code, 404)

        self.booking.refresh_from_db()
        self.assertEqual(self.booking.guests, 2)
        self.assertEqual(self.booking.owner_id, self.owner.pk)

    def test_anonymous_requests_cannot_access_booking_routes(self):
        self.client.logout()
        urls = [
            reverse("booking"), reverse("booking_list"),
            reverse("booking_success"), self.edit_url, self.delete_url,
        ]
        for url in urls:
            for method in [self.client.get, self.client.post]:
                with self.subTest(url=url, method=method.__name__):
                    response = method(url)
                    self.assertEqual(response.status_code, 302)
                    self.assertTrue(
                        response.url.startswith(reverse("login") + "?next=")
                    )
        self.assertEqual(Booking.objects.count(), 1)

    def test_delete_requires_confirmation_post(self):
        self.assertEqual(self.client.get(self.delete_url).status_code, 200)
        self.assertTrue(Booking.objects.filter(pk=self.booking.pk).exists())

        response = self.client.post(self.delete_url, follow=True)
        self.assertContains(response, "Booking deleted.")
        self.assertFalse(Booking.objects.filter(pk=self.booking.pk).exists())

    def test_post_without_csrf_token_is_rejected(self):
        client = Client(enforce_csrf_checks=True)
        client.force_login(self.owner)

        for url in [reverse("booking"), self.edit_url, self.delete_url]:
            with self.subTest(url=url):
                response = client.post(url, dict(self.data, guests=8))
                self.assertEqual(response.status_code, 403)

        self.assertEqual(Booking.objects.count(), 1)
        self.booking.refresh_from_db()
        self.assertEqual(self.booking.guests, 2)
