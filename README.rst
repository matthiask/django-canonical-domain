=================================================================
django-canonical-domain - Canonical domain redirection for Django
=================================================================

.. image:: https://travis-ci.org/matthiask/django-canonical-domain.png?branch=master
   :target: https://travis-ci.org/matthiask/django-canonical-domain

.. image:: https://readthedocs.org/projects/django-canonical-domain/badge/?version=latest
    :target: https://django-canonical-domain.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status

.. image:: https://codeclimate.com/github/matthiask/django-canonical-domain.png
    :target: https://codeclimate.com/github/matthiask/django-canonical-domain

This module allows redirecting all requests for a given Django instance
to a single canonical domain and optionally enforcing HTTPS for all
requests as well.

It achieves this by providing a replacement for Django's
``django.middleware.security.SecurityMiddleware`` which overrides its
request processing with a variant that also redirects requests to the
canonical domain which already are secure.

- `Documentation <https://django-canonical-domain.readthedocs.io>`_
- `Github <https://github.com/matthiask/django-canonical-domain/>`_
