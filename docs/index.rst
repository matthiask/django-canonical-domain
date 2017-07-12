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

django-canonical-domain offers two middleware classes:

- ``CanonicalDomainMiddleware`` does nothing but redirect all requests
  to the ``CANONICAL_DOMAIN`` setting while preserving the protocol,
  path and query string parts of the request.
- ``SecurityCanonicalDomainMiddleware`` extends Django's
  ``SecurityMiddleware`` with the added functionality of redirecting all
  requests to ``CANONICAL_DOMAIN`` (respectively ``SECURE_SSL_HOST``,
  but see below), not just insecure requests.


Installation
============

- ``pip install django-canonical-domain``
- Either

  - Add ``canonical_domain.middleware.CanonicalDomainMiddleware`` to
    your ``MIDDLEWARE`` setting (or ``MIDDLEWARE_CLASSES`` if you still
    are on a old school Django version)
  - Or replace the ``SecurityMiddleware`` with
    ``canonical_domain.middleware.SecurityCanonicalDomainMiddleware``

- If using ``CanonicalDomainMiddleware`` set ``CANONICAL_DOMAIN =
  'example.com'`` in your settings. The middleware does nothing if
  ``DEBUG`` is ``True``.
- If using ``SecurityCanonicalDomainMiddleware`` configure the
  ``SecurityMiddleware`` as you would without the canonical part. The
  middleware prefers the ``CANONICAL_DOMAIN`` setting over
  ``SECURE_SSL_HOST``, but apart from that configuration is exactly the
  same. Note that you probably also want to set ``SECURE_SSL_REDIRECT``
  to ``True``.

.. include:: ../CHANGELOG.rst
