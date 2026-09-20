from datetime import timedelta
from html.parser import HTMLParser
from urllib.parse import unquote, urljoin, urlsplit

from django.contrib.auth import get_user_model
from django.contrib.staticfiles import finders
from django.test import TestCase, override_settings
from django.urls import resolve, reverse
from django.utils import timezone

from .models import Booking, MenuItem


class PageParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []
        self.assets = []
        self.actions = []
        self.labels = []
        self.input_ids = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)

        if tag == "a" and attrs.get("href"):
            self.links.append(attrs["href"])

        if tag in ("img", "script") and attrs.get("src"):
            self.assets.append(attrs["src"])

        if tag == "link" and attrs.get("href"):
            self.assets.append(attrs["href"])

        if tag == "form":
            self.actions.append(attrs.get("action", ""))

        if tag == "label":
            self.labels.append(attrs.get("for"))

        if tag in ("input", "select", "textarea") and attrs.get("id"):
            self.input_ids.append(attrs["id"])


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
class PageLinkTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(username="link_tester")

        cls.booking = Booking.objects.create(
            owner=cls.user,
            name="Link Test",
            email="links@example.com",
            phone="+353 871234567",
            guests=2,
            date=timezone.localdate() + timedelta(days=3),
            time="12:00",
        )

        MenuItem.objects.create(
            name="Starters - Test Soup",
            description="Test menu item",
            price="5.00",
        )

    def pages(self):
        self.client.force_login(self.user)

        urls = [
            reverse("home"),
            reverse("menu"),
            reverse("booking"),
            reverse("booking_list"),
            reverse("booking_success"),
            reverse("edit_booking", args=[self.booking.pk]),
            reverse("delete_booking", args=[self.booking.pk]),
        ]

        for url in urls:
            yield url, self.parse_page(url)

        self.client.logout()

        for name in ["home", "menu", "login", "signup"]:
            url = reverse(name)
            yield url, self.parse_page(url)

    def parse_page(self, url):
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200, url)

        parser = PageParser()
        parser.feed(response.content.decode())
        return parser

    def local_url(self, page, target):
        absolute = urljoin("http://testserver" + page, target)
        parts = urlsplit(absolute)

        if parts.scheme not in ("http", "https"):
            return None

        if parts.netloc != "testserver":
            return None

        return parts.path + ("?" + parts.query if parts.query else "")

    def test_internal_links_and_form_action_routes(self):
        for page, parsed in self.pages():
            for target in parsed.links:
                url = self.local_url(page, target)

                if url is not None:
                    with self.subTest(page=page, link=target):
                        response = self.client.get(url, follow=True)
                        self.assertEqual(response.status_code, 200)

            for target in parsed.actions:
                url = self.local_url(page, target)
                self.assertIsNotNone(url, "Unexpected external form action")
                resolve(urlsplit(url).path)

    def test_referenced_local_static_assets_exist(self):
        for page, parsed in self.pages():
            for target in parsed.assets:
                url = self.local_url(page, target)

                if url is not None:
                    path = unquote(urlsplit(url).path)

                    with self.subTest(page=page, asset=target):
                        self.assertTrue(path.startswith("/static/"))
                        self.assertTrue(finders.find(path[len("/static/"):]))

    def test_create_and_edit_labels_match_field_ids(self):
        self.client.force_login(self.user)

        for url in [
            reverse("booking"),
            reverse("edit_booking", args=[self.booking.pk]),
        ]:
            parsed = self.parse_page(url)

            for field in ["name", "email", "phone", "guests", "date", "time"]:
                with self.subTest(page=url, field=field):
                    field_id = "id_" + field
                    self.assertIn(field_id, parsed.input_ids)
                    self.assertIn(field_id, parsed.labels)
