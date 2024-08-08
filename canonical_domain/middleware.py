import re

from django.apps import apps
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.http import HttpResponsePermanentRedirect
from django.utils.module_loading import import_string


if not apps.is_installed("canonical_domain"):
    raise ImproperlyConfigured(
        'Add "canonical_domain" to INSTALLED_APPS so that the bundled'
        " system checks can be registered."
    )


def canonical_domain(get_response):
    if not settings.SECURE_SSL_HOST:
        return get_response

    # List of regex patterns for paths that should not be redirected
    path_exempt = [
        re.compile(r) for r in getattr(settings, "SECURE_REDIRECT_EXEMPT", [])
    ]

    if exempt := getattr(
        settings,
        "CANONICAL_DOMAIN_EXEMPT",
        lambda response: False,
    ):
        exempt = exempt if callable(exempt) else import_string(exempt)

    def middleware(request):
        host = settings.SECURE_SSL_HOST
        secure_redirect = settings.SECURE_SSL_REDIRECT

        # Only redirect safe methods according to the RFC:
        # https://tools.ietf.org/html/rfc7231#section-4.2.1
        if request.method not in {
            "GET",
            "HEAD",
            "OPTIONS",
            "TRACE",
        }:
            return get_response(request)

        matches = request.get_host() == host
        is_secure = request.is_secure()

        # Simple case. Host matches and we do not have to redirect to secure
        # (maybe because we already are).
        if matches and (is_secure or not secure_redirect):
            return get_response(request)

        # Request may be exempt from redirects.
        is_exempt = exempt(request)
        if is_exempt and (is_secure or not secure_redirect):
            return get_response(request)

        # Path is exempt from redirects.
        path = request.path.lstrip("/")
        if any(pattern.search(path) for pattern in path_exempt):
            if matches or is_exempt:
                return get_response(request)
            secure_redirect = False

        return HttpResponsePermanentRedirect(
            "http%s://%s%s"
            % (
                "s" if is_secure or secure_redirect else "",
                request.get_host() if is_exempt else host,
                request.get_full_path(),
            )
        )

    return middleware
