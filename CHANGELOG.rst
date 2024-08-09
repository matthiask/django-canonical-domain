Change log
==========

Next version
~~~~~~~~~~~~


0.11 (2024-08-09)
~~~~~~~~~~~~~~~~~

- Changed ``CANONICAL_DOMAIN_EXEMPT`` to be a function or a dotted Python path
  to a function instead of a list of regexes. It's more flexible.


0.10 (2024-08-08)
~~~~~~~~~~~~~~~~~

- Added the requirement that ``canonical_domain`` be added to
  ``INSTALLED_APPS`` because otherwise the system checks wouldn't run at all.
- Added deploy checks which verify that ``SECURE_SSL_HOST`` and
  ``SECURE_SSL_REDIRECT`` have been set.
- Added Django 5.1 to the CI matrix.
- Added support for Django's ``SECURE_REDIRECT_EXEMPT`` setting and support for
  adding additional hosts which shouldn't be redirected. Thanks @PetrDlouhy!


`0.9`_ (2022-01-31)
~~~~~~~~~~~~~~~~~~~

- Added pre-commit.
- Dropped support for Django < 3.2, Python < 3.8, added support for Django 4.0
  and Python 3.10.
- Switched back to using ``SECURE_SSL_REDIRECT`` and ``SECURE_SSL_HOST`` --
  introducing our own settings made it necessary to silence Django's system
  checks for them. Let's not do that anymore. Added system checks to ensure
  that the new settings are added correctly.
- Added a system check which verifies that the canonical domain middleware
  appears before the security middleware in ``MIDDLEWARE``.


`0.4`_ (2021-07-20)
~~~~~~~~~~~~~~~~~~~

- Dropped official support for Django < 2.2 and Python < 3.6.
- Switched to a declarative setup.
- Switched to GitHub actions.
- Replaced the ``CanonicalDomainMiddleware`` with a new function-based
  ``canonical_domain`` middleware which does not extend ``SecurityMiddleware``.
  You should add ``SecurityMiddleware`` yourself and remove the silencing of
  ``security.W001``.


`0.3`_ (2018-12-24)
~~~~~~~~~~~~~~~~~~~

- Removed the self-deactivation of the middleware when ``DEBUG = True``.
- Reformatted the code using black.
- Changed the middleware to only redirect safe methods (``GET``,
  ``HEAD``, ``OPTIONS`` and ``TRACE``).


`0.2`_ (2017-07-12)
~~~~~~~~~~~~~~~~~~~

- Merged ``CanonicalDomainMiddleware`` and
  ``SecurityCanonicalDomainMiddleware`` and added a new setting
  ``CANONICAL_DOMAIN_SECURE`` which replaces our usage of
  ``SECURE_SSL_REDIRECT``.
- Added some documentation.
- Fixed links in the changelog.


`0.1`_ (2017-07-12)
~~~~~~~~~~~~~~~~~~~

- Initial public version.

.. _0.1: https://github.com/matthiask/django-canonical-domain/commit/55721303fc
.. _0.2: https://github.com/matthiask/django-canonical-domain/compare/0.1...0.2
.. _0.3: https://github.com/matthiask/django-canonical-domain/compare/0.2...0.3
.. _0.4: https://github.com/matthiask/django-canonical-domain/compare/0.3...0.4
.. _0.9: https://github.com/matthiask/django-canonical-domain/compare/0.4...0.9
.. _Next version: https://github.com/matthiask/django-canonical-domain/compare/0.9...master
