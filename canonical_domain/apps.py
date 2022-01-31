from django.apps import AppConfig
from django.conf import settings
from django.core.checks import Error, Tags, register


class CanonicalDomainAppConfig(AppConfig):
    name = "canonical_domain"

    def ready(self):
        register(Tags.security)(check)


def check(**kwargs):
    errors = []
    errors.extend(_check_ordering())
    errors.extend(_check_removed_settings())
    return errors


def _check_ordering():
    try:
        index_1 = settings.MIDDLEWARE.index(
            "canonical_domain.middleware.canonical_domain"
        )
        index_2 = settings.MIDDLEWARE.index(
            "django.middleware.security.SecurityMiddleware"
        )
    except ValueError:
        pass
    else:
        if index_1 > index_2:
            yield Error(
                "The canonical_domain middleware must appear before the"
                " SecurityMiddleware in MIDDLEWARE.",
                id="canonical_domain.E001",
            )


def _check_removed_settings():
    if hasattr(settings, "CANONICAL_DOMAIN"):
        yield Error(
            "You are using the removed CANONICAL_DOMAIN setting.",
            hint="Replace CANONICAL_DOMAIN with SECURE_SSL_HOST.",
            id="canonical_domain.E002",
        )
    if hasattr(settings, "CANONICAL_DOMAIN_SECURE"):
        yield Error(
            "You are using the removed CANONICAL_DOMAIN_SECURE setting.",
            hint="Replace CANONICAL_DOMAIN_SECURE with SECURE_SSL_REDIRECT.",
            id="canonical_domain.E003",
        )
