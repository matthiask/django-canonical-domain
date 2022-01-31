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
    secure = getattr(settings, "SECURE_SSL_REDIRECT", False)

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

        matches = request.get_host() == host

        if matches and secure and request.is_secure():
            return get_response(request)
        elif matches and not secure:
            return get_response(request)

        return HttpResponsePermanentRedirect(
            "http%s://%s%s"
            % (
                "s" if (secure or request.is_secure()) else "",
                host,
                request.get_full_path(),
            )
        )

    return middleware
