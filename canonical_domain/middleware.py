import re

from django.apps import apps
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.http import HttpResponsePermanentRedirect


if not apps.is_installed("canonical_domain"):
    raise ImproperlyConfigured(
        'Add "canonical_domain" to INSTALLED_APPS so that the bundled'
        " system checks can be registered."
    )


def canonical_domain(get_response):
    host = getattr(settings, "SECURE_SSL_HOST", "")
    secure_redirect = getattr(settings, "SECURE_SSL_REDIRECT", False)

    # List of complete domains such as r'^api.example.com$'
    host_exempt = [
        re.compile(r) for r in getattr(settings, "CANONICAL_DOMAIN_EXEMPT", [])
    ]

    # List of regex patterns for paths that should not be redirected
    path_exempt = [
        re.compile(r) for r in getattr(settings, "SECURE_REDIRECT_EXEMPT", [])
    ]

    if not host:
        return get_response

    def middleware(request):
        # Only redirect safe methods according to the RFC:
        # https://tools.ietf.org/html/rfc7231#section-4.2.1
        if not host or request.method not in {
            "GET",
            "HEAD",
            "OPTIONS",
            "TRACE",
        }:
            return get_response(request)

        path = request.path.lstrip("/")
        secure_changes = not any(pattern.search(path) for pattern in path_exempt)
        is_secure = (
            (secure_redirect or request.is_secure())
            if secure_changes
            else request.is_secure()
        )

        matches = request.get_host() == host

        if matches and (
            (secure_redirect and request.is_secure())
            or not secure_redirect
            or not secure_changes
        ):
            return get_response(request)

        if any(pattern.search(request.get_host()) for pattern in host_exempt):
            if secure_redirect and not request.is_secure():
                return HttpResponsePermanentRedirect(
                    "https://%s%s" % (request.get_host(), request.get_full_path())
                )
            return get_response(request)

        return HttpResponsePermanentRedirect(
            "http%s://%s%s"
            % (
                "s" if is_secure else "",
                host,
                request.get_full_path(),
            )
        )

    return middleware
