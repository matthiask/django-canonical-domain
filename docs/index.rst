=================================================================
django-canonical-domain - Canonical domain redirection for Django
=================================================================

Version |release|

This module allows redirecting all requests for a given Django instance
to a single canonical domain and optionally enforcing HTTPS for all
requests as well.


Installation and usage
======================

- ``pip install django-canonical-domain``
- Add ``canonical_domain.middleware.canonical_domain`` to your ``MIDDLEWARE``
  setting. Ensure that you add this middleware *before*
  ``django.middleware.security.SecurityMiddleware``.
- Set ``CANONICAL_DOMAIN = 'example.com'`` in your settings.
- Optionally set ``CANONICAL_DOMAIN_SECURE = True`` if you want to
  enforce HTTPS.
- Set additional ``SECURE_*`` settings -- all settings are valid and
  supported except for ``SECURE_SSL_REDIRECT`` and ``SECURE_SSL_HOST``.


.. include:: ../CHANGELOG.rst
