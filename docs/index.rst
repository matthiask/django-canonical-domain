=================================================================
django-canonical-domain - Canonical domain redirection for Django
=================================================================

Version |release|

This module allows redirecting all requests for a given Django instance
to a single canonical domain and optionally enforcing HTTPS for all
requests as well.

It achieves this by providing a replacement for Django's
``django.middleware.security.SecurityMiddleware`` which overrides its
request processing with a variant that also redirects requests to the
canonical domain which already are secure.


Installation and usage
======================

- ``pip install django-canonical-domain``
- Add ``canonical_domain.middleware.CanonicalDomainMiddleware`` to your
  ``MIDDLEWARE`` setting (or ``MIDDLEWARE_CLASSES`` if you still are on
  a old school Django version)
- Set ``CANONICAL_DOMAIN = 'example.com'`` in your settings.
- Optionally set ``CANONICAL_DOMAIN_SECURE = True`` if you want to
  enforce HTTPS.
- Set additional ``SECURE_*`` settings -- all settings are valid and
  supported except for ``SECURE_SSL_REDIRECT`` and ``SECURE_SSL_HOST``.

Note that the middleware does nothing if ``DEBUG`` is ``True`` or if
``CANONICAL_DOMAIN`` is not set.


.. include:: ../CHANGELOG.rst
