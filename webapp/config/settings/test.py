from .base import *

DEBUG = True

SECRET_KEY = os.environ.get(
    "SECRET_KEY", "94n7fx27pd-!stt2fl@we!mn5=+-8l#!kber_j&p4s9hs+5w"
)

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ.get("NAME", "test_db"),
        "USER": os.environ.get("USER", "postgres"),
        "PASSWORD": os.environ.get("PASSWORD", "postgres"),
        "HOST": os.environ.get("HOST", "localhost"),
        "PORT": os.environ.get("PORT", "5432"),
    }
}
