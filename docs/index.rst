=================================================================
django-canonical-domain - Canonical domain redirection for Django
=================================================================

Version |release|


Installation
============

- ``pip install django-canonical-domain``
- Either

  - Add ``canonical_domain.middleware.CanonicalDomainMiddleware`` to your
    ``MIDDLEWARE`` setting (or ``MIDDLEWARE_CLASSES`` if you still are on
    a old school Django version)
  - Or replace the ``SecurityMiddleware`` with
    ``canonical_domain.middleware.SecurityCanonicalDomainMiddleware``

- If using ``CanonicalDomainMiddleware`` set ``CANONICAL_DOMAIN = 'example.com'``
  in your settings
- If using ``SecurityCanonicalDomainMiddleware`` configure the
  ``SecurityMiddleware``
  as you would without the canonical part. The middleware prefers
  the ``CANONICAL_DOMAIN`` setting to ``SECURE_SSL_HOST``, but apart from that
  configuration is exactly the same.

.. include:: ../CHANGELOG.rst
