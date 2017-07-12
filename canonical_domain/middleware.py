from __future__ import absolute_import, unicode_literals

from django.conf import settings
from django.core.exceptions import MiddlewareNotUsed
from django.http import HttpResponsePermanentRedirect
from django.middleware.security import SecurityMiddleware
from django.utils.deprecation import MiddlewareMixin


class CanonicalDomainMiddleware(MiddlewareMixin):
    def __init__(self, *args, **kwargs):
        super(CanonicalDomainMiddleware, self).__init__(*args, **kwargs)
        self.canonical_domain = getattr(settings, 'CANONICAL_DOMAIN', None)
        if settings.DEBUG or not self.canonical_domain:
            raise MiddlewareNotUsed

    def process_request(self, request):
        if request.get_host() == self.canonical_domain:
            return

        return HttpResponsePermanentRedirect('http%s://%s%s' % (
            's' if request.is_secure() else '',
            self.canonical_domain,
            request.get_full_path(),
        ))


class SecurityCanonicalDomainMiddleware(SecurityMiddleware):
    def __init__(self, *args, **kwargs):
        super(SecurityCanonicalDomainMiddleware, self).__init__(
            *args, **kwargs)
        self.redirect_host = (
            getattr(settings, 'CANONICAL_DOMAIN', None) or
            settings.SECURE_SSL_HOST
        )

    def process_request(self, request):
        # Django's SecurityMiddleware.process_request does not redirect to
        # SECURE_SSL_HOST if a request is already secure. Make it so.
        # See https://code.djangoproject.com/ticket/28359

        if not self.redirect:
            return
        if (request.is_secure() and (
                # redirect_host is not set OR
                not self.redirect_host or
                # host is already the same
                self.redirect_host == request.get_host())):
            return
        path = request.path.lstrip('/')
        if any(pattern.search(path) for pattern in self.redirect_exempt):
            return

        host = self.redirect_host or request.get_host()
        return HttpResponsePermanentRedirect(
            'https://%s%s' % (host, request.get_full_path())
        )
