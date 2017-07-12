=================================================================
django-canonical-domain - Canonical domain redirection for Django
=================================================================

Version |release|

This module offers middlewares which redirect all requests for a given
Django instance to a single canonical domain.

Django has almost but not quite a solution for this in
``django.middleware.security.SecurityMiddleware``'s ``SECURE_SSL_HOST``
setting, but this setting only affects redirects from HTTP to HTTPS.
Django also has ``PREPEND_WWW``, but this is not sufficient for
canonical domain redirects either.

django-canonical-domain offers a middleware which replaces Django's
``SecurityMiddleware`` request processing with a variant that redirects
all requests to ``CANONICAL_DOMAIN``, with optionally also enforcing
HTTPS (similar to ``SecurityMiddleware``'s ``SECURE_SSL_HOST`` and
``SECURE_SSL_REDIRECT`` settings) with the small but important
difference that requests which already are secure are redirected to the
canonical domain as well. (``SecurityMiddleware`` only redirects
insecure requests to ``SECURE_SSL_HOST``.)


Installation
============

- ``pip install django-canonical-domain``
- Add ``canonical_domain.middleware.CanonicalDomainMiddleware`` to your
  ``MIDDLEWARE`` setting (or ``MIDDLEWARE_CLASSES`` if you still are on
  a old school Django version)
- Set ``CANONICAL_DOMAIN = 'example.com'`` in your settings.
- Optionally set ``CANONICAL_DOMAIN_SECURE = True`` if you want to
  enforce HTTPS and any additional ``SECURE_*`` settings from Django
  proper.

Note that the middleware does nothing if ``DEBUG`` is ``True`` or if
``CANONICAL_DOMAIN`` is not set.


.. include:: ../CHANGELOG.rst
