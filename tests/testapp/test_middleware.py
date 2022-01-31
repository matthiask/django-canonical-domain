from django.test import TestCase
from django.test.utils import override_settings

from canonical_domain.middleware import check


@override_settings(MIDDLEWARE=["canonical_domain.middleware.canonical_domain"])
class MiddlewareNotUsedTestCase(TestCase):
    def test_request(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b"Hello world")


@override_settings(
    MIDDLEWARE=["canonical_domain.middleware.canonical_domain"],
    SECURE_SSL_HOST="example.com",
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
    SECURE_SSL_HOST="example.com",
    SECURE_SSL_REDIRECT=True,
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


class ChecksTestCase(TestCase):
    def assertCheckCodes(self, codes):
        self.assertEqual([obj.id for obj in check()], codes)

    @override_settings(
        MIDDLEWARE=[
            "canonical_domain.middleware.canonical_domain",
            "django.middleware.security.SecurityMiddleware",
        ],
        SECURE_SSL_HOST="example.com",
        SECURE_SSL_REDIRECT=True,
    )
    def test_valid(self):
        self.assertCheckCodes([])

    @override_settings(
        SECURE_SSL_HOST="example.com",
        SECURE_SSL_REDIRECT=True,
    )
    def test_invalid_middleware_setting(self):
        with override_settings(
            MIDDLEWARE=[
                "canonical_domain.middleware.canonical_domain",
                "django.middleware.security.SecurityMiddleware",
            ],
        ):
            self.assertCheckCodes([])

        with override_settings(
            MIDDLEWARE=[
                "django.middleware.security.SecurityMiddleware",
                "canonical_domain.middleware.canonical_domain",
            ],
        ):
            self.assertCheckCodes(["canonical_domain.E001"])

        with override_settings(
            MIDDLEWARE=[
                "canonical_domain.middleware.canonical_domain",
                # "django.middleware.security.SecurityMiddleware",
            ],
        ):
            self.assertCheckCodes([])

    def test_removed_settings(self):
        with override_settings(
            CANONICAL_DOMAIN="example.com",
        ):
            self.assertCheckCodes(["canonical_domain.E002"])

        with override_settings(
            CANONICAL_DOMAIN_SECURE="",  # Value isn't important
        ):
            self.assertCheckCodes(["canonical_domain.E003"])

        with override_settings(
            CANONICAL_DOMAIN="example.com",
            CANONICAL_DOMAIN_SECURE="",  # Value isn't important
        ):
            self.assertCheckCodes(["canonical_domain.E002", "canonical_domain.E003"])
