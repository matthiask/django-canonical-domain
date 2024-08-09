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
- ``django-canonical-domain`` also respects ``SECURE_REDIRECT_EXEMPT``
  settings. In the case path matches the regex the url will be redirected to
  ``SECURE_SSL_HOST``, but the protocol will not be changed.


Configuration
=============

``CANONICAL_DOMAIN_EXEMPT``

Default: ``None``

A function which receives the request object and returns ``True`` if the
request shouldn't be redirected to the canonical domain. HTTPS will still be
enforced when ``SECURE_SSL_REDIRECT`` is set.

If you want to allow ``api.example.com`` in addition to ``example.com`` you
could set ``CANONICAL_DOMAIN_EXEMPT = lambda request: request.get_host() ==
"api.example.com"``. The setting also supports a dotted Python path to a
function.


.. include:: ../CHANGELOG.rst
