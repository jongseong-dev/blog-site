from .base import *

DEBUG = True

INSTALLED_APPS += [
    "debug_toolbar",
]
SECRET_KEY = os.environ.get(
    "SECRET_KEY", "94n7fx27pd-!stt2fl@we!mn5=+-8l#!kber_j&p4s9hs+5w"
)
MIDDLEWARE += [
    "debug_toolbar.middleware.DebugToolbarMiddleware",
]

INTERNAL_IPS = [
    "127.0.0.1",
]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ.get("NAME", "postgres"),
        "USER": os.environ.get("USER", "postgres"),
        "PASSWORD": os.environ.get("PASSWORD", "postgres"),
        "HOST": os.environ.get("HOST", "localhost"),
        "PORT": os.environ.get("PORT", "5432"),
    }
}
