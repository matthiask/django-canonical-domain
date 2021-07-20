from django.conf import settings
from django.http import HttpResponsePermanentRedirect


def canonical_domain(get_response):
    canonical_domain = getattr(settings, "CANONICAL_DOMAIN", "")
    canonical_domain_secure = getattr(settings, "CANONICAL_DOMAIN_SECURE", False)

    if not canonical_domain:
        return get_response

    def middleware(request):
        # Only redirect safe methods according to the RFC:
        # https://tools.ietf.org/html/rfc7231#section-4.2.1
        if not canonical_domain or request.method not in {
            "GET",
            "HEAD",
            "OPTIONS",
            "TRACE",
        }:
            return get_response(request)

        matches = request.get_host() == canonical_domain

        if matches and canonical_domain_secure and request.is_secure():
            return get_response(request)
        elif matches and not canonical_domain_secure:
            return get_response(request)

        return HttpResponsePermanentRedirect(
            "http%s://%s%s"
            % (
                "s" if (canonical_domain_secure or request.is_secure()) else "",
                canonical_domain,
                request.get_full_path(),
            )
        )

    return middleware
