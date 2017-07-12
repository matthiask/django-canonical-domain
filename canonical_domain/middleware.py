from __future__ import absolute_import, unicode_literals

from django.conf import settings
from django.core.exceptions import MiddlewareNotUsed
from django.http import HttpResponsePermanentRedirect
from django.middleware.security import SecurityMiddleware


class CanonicalDomainMiddleware(SecurityMiddleware):
    canonical_domain = None
    canonical_domain_secure = None

    def __init__(self, *args, **kwargs):
        super(CanonicalDomainMiddleware, self).__init__(*args, **kwargs)
        try:
            self.canonical_domain = settings.CANONICAL_DOMAIN
            self.canonical_domain_secure = settings.CANONICAL_DOMAIN_SECURE
        except AttributeError:
            pass

        if settings.DEBUG or not self.canonical_domain:
            raise MiddlewareNotUsed

    def process_request(self, request):
        matches = request.get_host() == self.canonical_domain
        if matches and self.canonical_domain_secure and request.is_secure():
            return
        elif matches and not self.canonical_domain_secure:
            return

        return HttpResponsePermanentRedirect('http%s://%s%s' % (
            's' if (
                self.canonical_domain_secure or request.is_secure()
            ) else '',
            self.canonical_domain,
            request.get_full_path(),
        ))
