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
- Add ``canonical_domain`` to ``INSTALLED_APPS`` and
  ``canonical_domain.middleware.canonical_domain`` to your ``MIDDLEWARE``
  setting. Ensure that you add this middleware *before*
  ``django.middleware.security.SecurityMiddleware``.
- Set ``SECURE_SSL_HOST = 'example.com'`` in your settings.
- Optionally set ``SECURE_SSL_REDIRECT = True`` if you want to
  enforce HTTPS.


.. include:: ../CHANGELOG.rst
