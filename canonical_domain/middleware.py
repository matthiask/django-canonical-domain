from __future__ import absolute_import, unicode_literals

from django.conf import settings
from django.core.exceptions import MiddlewareNotUsed
from django.http import HttpResponsePermanentRedirect
from django.middleware.security import SecurityMiddleware


class CanonicalDomainMiddleware(SecurityMiddleware):
    def __init__(self, *args, **kwargs):
        super(CanonicalDomainMiddleware, self).__init__(*args, **kwargs)
        self.canonical_domain = getattr(settings, 'CANONICAL_DOMAIN', None)
        self.canonical_domain_secure = getattr(
            settings,
            'CANONICAL_DOMAIN_SECURE',
            False,
        )
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
