from django.conf import settings
from django.core.checks import Error, Tags, register
from django.http import HttpResponsePermanentRedirect


@register(Tags.security, deploy=True)
def check(**kwargs):
    errors = []
    errors.extend(_check_ordering())
    errors.extend(_check_removed_settings())
    return errors


def _check_ordering():
    try:
        index_1 = settings.MIDDLEWARE.index(
            "canonical_domain.middleware.canonical_domain"
        )
        index_2 = settings.MIDDLEWARE.index(
            "django.middleware.security.SecurityMiddleware"
        )
    except ValueError:
        pass
    else:
        if index_1 > index_2:
            yield Error(
                "The canonical_domain middleware must appear before the"
                " SecurityMiddleware in MIDDLEWARE.",
                id="canonical_domain.E001",
            )


def _check_removed_settings():
    if hasattr(settings, "CANONICAL_DOMAIN"):
        yield Error(
            "You are using the removed CANONICAL_DOMAIN setting.",
            hint="Replace CANONICAL_DOMAIN with SECURE_SSL_HOST.",
            id="canonical_domain.E002",
        )
    if hasattr(settings, "CANONICAL_DOMAIN_SECURE"):
        yield Error(
            "You are using the removed CANONICAL_DOMAIN_SECURE setting.",
            hint="Replace CANONICAL_DOMAIN_SECURE with SECURE_SSL_REDIRECT.",
            id="canonical_domain.E003",
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
