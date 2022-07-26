from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-9d^uhe)04$&!59%&u6x8+^8ub7c(dhs-*!hpoy62zp%%7_3m7$"

# SECURITY WARNING: define the correct hosts in production!
ALLOWED_HOSTS = ["*"]

INTERNAL_IPS = [
    # ...
    "127.0.0.1",
    # ...
]

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

try:
    from .local import *
except ImportError:
    pass
