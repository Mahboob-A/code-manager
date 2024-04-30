from .base import *  # noqa
from .base import env  # noqa: E501

# warnigns for linters code - E501 for unused variables


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env(
    "DJANGO_SECRET_KEY",
    default="django-insecure-!c=ip7oq+2mojk#6bg#whq45!05+t^^5&6$q4c87!5eg8p2for",
)

DEBUG = True

CSRF_TRUSTED_ORIGINS = ["http://localhost:8080", "http://127.0.0.1:8080"]

ALLOWED_HOSTS = ["127.0.0.1"]
