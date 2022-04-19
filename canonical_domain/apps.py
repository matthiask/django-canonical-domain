from django.apps import AppConfig
from django.conf import settings
from django.core.checks import Error, Tags, Warning, register


class CanonicalDomainAppConfig(AppConfig):
    name = "canonical_domain"

    def ready(self):
        register(Tags.security)(default_checks)
        register(Tags.security, deploy=True)(deploy_checks)


def default_checks(**kwargs):
    errors = []
    errors.extend(_check_ordering())
    errors.extend(_check_removed_settings())
    return errors


def deploy_checks(**kwargs):
    errors = []
    errors.extend(_check_deployment_settings())
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


def _check_deployment_settings():
    if not settings.SECURE_SSL_HOST:
        yield Warning(
            "SECURE_SSL_HOST is not set.",
            id="canonical_domain.W004",
        )
    if not settings.SECURE_SSL_REDIRECT:
        yield Warning(
            "SECURE_SSL_REDIRECT is not set to True.",
            id="canonical_domain.W005",
        )
