import os


BASE_DIR = os.path.dirname(os.path.dirname(__file__))

DATABASES = {"default": {"ENGINE": "django.db.backends.sqlite3", "NAME": ":memory:"}}

INSTALLED_APPS = ["testapp", "canonical_domain"]

BASEDIR = os.path.dirname(__file__)
SECRET_KEY = "supersikret"
ROOT_URLCONF = "testapp.urls"
ALLOWED_HOSTS = ["*"]
