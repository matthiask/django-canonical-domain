from __future__ import absolute_import, unicode_literals

from django.test import TestCase
from django.test.utils import override_settings


@override_settings(
    MIDDLEWARE=[
        'canonical_domain.middleware.CanonicalDomainMiddleware',
    ],
)
class MiddlewareNotUsedTestCase(TestCase):
    def test_request(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b'Hello world')


@override_settings(
    CANONICAL_DOMAIN='example.com',
    MIDDLEWARE=[
        'canonical_domain.middleware.CanonicalDomainMiddleware',
    ],
)
class CanonicalDomainMiddlewareTestCase(TestCase):
    def test_middleware(self):
        response = self.client.get(
            '/',
            HTTP_HOST='www.example.com',
        )
        self.assertEqual(response.status_code, 301)
        self.assertEqual(response['Location'], 'http://example.com/')

        response = self.client.get(
            '/',
            HTTP_HOST='example.com',
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b'Hello world')


@override_settings(
    MIDDLEWARE=[
        'canonical_domain.middleware.SecurityCanonicalDomainMiddleware',
    ],
)
class UnusedSecurityCanonicalDomainMiddlewareTestCase(TestCase):
    def test_request(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b'Hello world')


@override_settings(
    MIDDLEWARE=[
        'canonical_domain.middleware.SecurityCanonicalDomainMiddleware',
    ],
    SECURE_SSL_REDIRECT=True,
    SECURE_SSL_HOST='example.com',
)
class SecurityCanonicalDomainMiddlewareTestCase(TestCase):
    def test_middleware(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 301)
        self.assertEqual(response['Location'], 'https://example.com/')

        response = self.client.get(
            '/',
            HTTP_HOST='www.example.com',
        )
        self.assertEqual(response.status_code, 301)
        self.assertEqual(response['Location'], 'https://example.com/')

        response = self.client.get(
            '/',
            HTTP_HOST='example.com',
            secure=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b'Hello world')

        # This is the difference to Django's SecurityMiddleware redirect
        # behavior
        response = self.client.get(
            '/',
            HTTP_HOST='www.example.com',
            secure=True,
        )
        self.assertEqual(response.status_code, 301)
        self.assertEqual(response['Location'], 'https://example.com/')
