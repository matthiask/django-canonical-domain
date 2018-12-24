Change log
==========

`Next version`_
~~~~~~~~~~~~~~~

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
.. _0.2: https://github.com/matthiask/django-canonical-domain/compare/0.2...0.3
.. _Next version: https://github.com/matthiask/django-canonical-domain/compare/0.3...master
