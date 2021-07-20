from django.test import TestCase
from django.test.utils import override_settings


@override_settings(MIDDLEWARE=["canonical_domain.middleware.canonical_domain"])
class MiddlewareNotUsedTestCase(TestCase):
    def test_request(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b"Hello world")


@override_settings(
    MIDDLEWARE=["canonical_domain.middleware.canonical_domain"],
    CANONICAL_DOMAIN="example.com",
)
class CanonicalDomainTestCase(TestCase):
    def test_http_requests(self):
        response = self.client.get("/", HTTP_HOST="example.org")
        self.assertEqual(response.status_code, 301)
        self.assertEqual(response["Location"], "http://example.com/")

        response = self.client.get("/", HTTP_HOST="example.com")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b"Hello world")

        response = self.client.post("/", HTTP_HOST="example.org")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b"Hello world")

    def test_https_requests(self):
        response = self.client.get("/", HTTP_HOST="example.org", secure=True)
        self.assertEqual(response.status_code, 301)
        self.assertEqual(response["Location"], "https://example.com/")

        response = self.client.get("/", HTTP_HOST="example.com", secure=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b"Hello world")


@override_settings(
    MIDDLEWARE=["canonical_domain.middleware.canonical_domain"],
    CANONICAL_DOMAIN="example.com",
    CANONICAL_DOMAIN_SECURE=True,
)
class CanonicalDomainSecureTestCase(TestCase):
    def test_http_redirects(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 301)
        self.assertEqual(response["Location"], "https://example.com/")

        response = self.client.get("/", HTTP_HOST="example.org")
        self.assertEqual(response.status_code, 301)
        self.assertEqual(response["Location"], "https://example.com/")

    def test_https_redirects(self):
        response = self.client.get("/", HTTP_HOST="example.org", secure=True)
        self.assertEqual(response.status_code, 301)
        self.assertEqual(response["Location"], "https://example.com/")

    def test_match(self):
        response = self.client.get("/", HTTP_HOST="example.com", secure=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b"Hello world")
