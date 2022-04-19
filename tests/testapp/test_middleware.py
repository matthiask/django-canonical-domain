from django.test import TestCase
from django.test.utils import override_settings

from canonical_domain.apps import default_checks, deploy_checks


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
    def assertCheckCodes(self, check_results, codes):
        self.assertEqual([obj.id for obj in check_results], codes)

    @override_settings(
        MIDDLEWARE=[
            "canonical_domain.middleware.canonical_domain",
            "django.middleware.security.SecurityMiddleware",
        ],
        SECURE_SSL_HOST="example.com",
        SECURE_SSL_REDIRECT=True,
    )
    def test_valid(self):
        self.assertCheckCodes(default_checks(), [])

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
            self.assertCheckCodes(default_checks(), [])

        with override_settings(
            MIDDLEWARE=[
                "django.middleware.security.SecurityMiddleware",
                "canonical_domain.middleware.canonical_domain",
            ],
        ):
            self.assertCheckCodes(default_checks(), ["canonical_domain.E001"])

        with override_settings(
            MIDDLEWARE=[
                "canonical_domain.middleware.canonical_domain",
                # "django.middleware.security.SecurityMiddleware",
            ],
        ):
            self.assertCheckCodes(default_checks(), [])

    def test_removed_settings(self):
        with override_settings(
            CANONICAL_DOMAIN="example.com",
        ):
            self.assertCheckCodes(default_checks(), ["canonical_domain.E002"])

        with override_settings(
            CANONICAL_DOMAIN_SECURE="",  # Value isn't important
        ):
            self.assertCheckCodes(default_checks(), ["canonical_domain.E003"])

        with override_settings(
            CANONICAL_DOMAIN="example.com",
            CANONICAL_DOMAIN_SECURE="",  # Value isn't important
        ):
            self.assertCheckCodes(
                default_checks(), ["canonical_domain.E002", "canonical_domain.E003"]
            )

    def test_deploy_settings(self):
        self.assertCheckCodes(
            deploy_checks(), ["canonical_domain.W004", "canonical_domain.W005"]
        )
        with override_settings(
            SECURE_SSL_HOST="example.com",
            SECURE_SSL_REDIRECT=True,
        ):
            self.assertCheckCodes(deploy_checks(), [])
