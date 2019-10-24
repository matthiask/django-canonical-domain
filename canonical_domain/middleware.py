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
        self.allowed_subdomains = getattr(
            settings, "CANONICAL_DOMAIN_ALLOWED_SUBDOMAINS", []
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
        host = request.get_host()
        matches = host == self.canonical_domain or any(
            map(
                lambda x: ("%s.%s" % (x, self.canonical_domain) == host),
                self.allowed_subdomains,
            )
        )
        if matches and self.canonical_domain_secure and request.is_secure():
            return
        elif matches and not self.canonical_domain_secure:
            return

        canonical_subdomain = next(
            (sub for sub in self.allowed_subdomains if sub in host), None
        )

        return HttpResponsePermanentRedirect(
            "http%s://%s%s%s"
            % (
                "s" if (self.canonical_domain_secure or request.is_secure()) else "",
                "%s." % canonical_subdomain if canonical_subdomain is not None else "",
                self.canonical_domain,
                request.get_full_path(),
            )
        )
