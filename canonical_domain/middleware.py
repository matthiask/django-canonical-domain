from __future__ import absolute_import, unicode_literals

from django.conf import settings
from django.http import HttpResponsePermanentRedirect
from django.middleware.security import SecurityMiddleware


class CanonicalDomainMiddleware(SecurityMiddleware):
    canonical_domain = None
    canonical_domain_secure = None

    def __init__(self, *args, **kwargs):
        super(CanonicalDomainMiddleware, self).__init__(*args, **kwargs)
        self.canonical_domain = getattr(settings, "CANONICAL_DOMAIN", "")
        self.canonical_domain_secure = getattr(
            settings, "CANONICAL_DOMAIN_SECURE", False
        )

    def process_request(self, request):
        # Only redirect safe methods according to the RFC:
        # https://tools.ietf.org/html/rfc7231#section-4.2.1
        if not self.canonical_domain or request.method not in {
            "GET",
            "HEAD",
            "OPTIONS",
            "TRACE",
        }:
            return

        matches = request.get_host() == self.canonical_domain
        if matches and self.canonical_domain_secure and request.is_secure():
            return
        elif matches and not self.canonical_domain_secure:
            return

        return HttpResponsePermanentRedirect(
            "http%s://%s%s"
            % (
                "s" if (self.canonical_domain_secure or request.is_secure()) else "",
                self.canonical_domain,
                request.get_full_path(),
            )
        )
