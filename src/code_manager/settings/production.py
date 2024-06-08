from .base import *  # noqa
from .base import env  # noqa: E501

# warnigns for linters code - E501 for unused variables


# Django project general settings.
ADMINS = [("Mahboob Alam", "iammahboob.a@gmail.com")]
SECRET_KEY = env("DJANGO_SECRET_KEY")
ADMIN_URL = env("ADMIN_URL")
DATABASES = {"default": env.db("DATABASE_URL")}


# Django security settings.
ALLOWED_HOSTS = env.list("DJANGO_ALLOWED_HOSTS", default=["codemanager.algocode.site"])

# TODO  for testing prod locally 
# ALLOWED_HOSTS = ["127.0.0.1"]

CSRF_TRUSTED_ORIGINS = [
    "https://codemanager.algocode.site",
    "https://algocode.site",
    "http://127.0.0.1:8080",  # for testing prod locally 
]

SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

SECURE_SSL_REDIRECT = env("DJANGO_SECURE_SSL_REDIRECT", default=True)


# TODO caution. 518400 seconds as 6 days. 
SECURE_HSTS_SECONDS = 518400  

SECURE_HSTS_INCLUDE_SUBDOMAINS = env.bool(
    "DJANGO_SECURE_HSTS_INCLUDE_SUBDOMAINS", default=True
)

SECURE_CONTENT_TYPE_NOSNIFF = env.bool(
    "DJANGO_SECURE_CONTENT_TYPE_NOSNIFF", default=True
)

# Static file content host
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

SITE_NAME = "Algocode - The Modern Leetcode!"


####################################################### Config Settings

# Time to cache the code execution result in redis
REDIS_CACHE_HOST = env("REDIS_CACHE_HOST")

REDIS_CACHE_RATELIMIT_DB_INDEX = int(env("REDIS_CACHE_RATELIMIT_DB_INDEX"))
REDIS_CACHE_RESULT_DB_INDEX = int(env("REDIS_CACHE_RESULT_DB_INDEX"))

# cache timeout for code exec result
REDIS_CODE_EXEC_RESULT_CACHE_TIME_IN_SECONDS = int(
    env("REDIS_CODE_EXEC_RESULT_CACHE_TIME_IN_SECONDS")
)

# cache timeout for code submit api rate limit
REDIS_RATE_LIMIT_CACHE_TIME_IN_SECONDS = int(
    env("REDIS_RATE_LIMIT_CACHE_TIME_IN_SECONDS")
)

# Code Submit API path.
CODE_SUBMIT_API_PATH = "/api/v1/code/submit/"

# Config for MQ: Code Submission Publish
CLOUD_AMQP_URL = env("CLOUD_AMQP_URL")

# Config for Cpp Queue
CPP_CODE_SUBMISSION_EXCHANGE_NAME = env("CPP_CODE_SUBMISSION_EXCHANGE_NAME")
CPP_CODE_SUBMISSION_EXCHANGE_TYPE = env("CPP_CODE_SUBMISSION_EXCHANGE_TYPE")
CPP_CODE_SUBMISSION_QUEUE_NAME = env("CPP_CODE_SUBMISSION_QUEUE_NAME")
CPP_CODE_SUBMISSION_BINDING_KEY = env("CPP_CODE_SUBMISSION_BINDING_KEY")
CPP_CODE_SUBMISSION_ROUTING_KEY = env("CPP_CODE_SUBMISSION_ROUTING_KEY")

# Config for Java Queue
JAVA_CODE_SUBMISSION_EXCHANGE_NAME = env("JAVA_CODE_SUBMISSION_EXCHANGE_NAME")
JAVA_CODE_SUBMISSION_EXCHANGE_TYPE = env("JAVA_CODE_SUBMISSION_EXCHANGE_TYPE")
JAVA_CODE_SUBMISSION_QUEUE_NAME = env("JAVA_CODE_SUBMISSION_QUEUE_NAME")
JAVA_CODE_SUBMISSION_BINDING_KEY = env("JAVA_CODE_SUBMISSION_BINDING_KEY")
JAVA_CODE_SUBMISSION_ROUTING_KEY = env("JAVA_CODE_SUBMISSION_ROUTING_KEY")


# Config for MQ: Result Publish Consume
RESULT_PUBLISH_EXCHANGE_NAME = env("RESULT_PUBLISH_EXCHANGE_NAME")
RESULT_PUBLISH_EXCHANGE_TYPE = env("RESULT_PUBLISH_EXCHANGE_TYPE")
RESULT_PUBLISH_QUEUE_NAME = env("RESULT_PUBLISH_QUEUE_NAME")
RESULT_PUBLISH_BINDING_KEY = env("RESULT_PUBLISH_BINDING_KEY")
RESULT_PUBLISH_ROUTING_KEY = env("RESULT_PUBLISH_ROUTING_KEY")


# mongo settings
MONGO_HOST = env("MONGO_HOST")
MONGO_PORT = int(env("MONGO_PORT"))
MONGO_DB_NAME = env(
    "MONGO_INITDB_DATABASE",
)
MONGO_USER = env("MONGO_INITDB_ROOT_USERNAME")
MONGO_PASS = env("MONGO_INITDB_ROOT_PASSWORD")
MONGO_RESULT_COLLECTIOIN = env("MONGO_INITDB_COLLECTION")
MONGO_AUTH_SOURCE_DB = env("MONGO_AUTH_SOURCE_DB")


########################################################
# logging
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "filters": {"require_debug_false": {"()": "django.utils.log.RequireDebugFalse"}},
    "formatters": {
        "verbose": {
            "format": "%(levelname)s  %(asctime)s %(module)s  %(process)d %(thread)d %(message)s "
        }
    },
    "handlers": {
        "mail_admins": {
            "level": "ERROR",
            "filters": ["require_debug_false"],
            "class": "django.utils.log.AdminEmailHandler",
        },
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        },
    },
    "root": {
        "level": "INFO",
        "handlers": ["console"],
    },
    "loggers": {
        "django.request": {  # only used when debug=false
            "handlers": ["mail_admins"],
            "level": "ERROR",
            "propagate": True,
        },
        "django.security.DisallowedHost": {  # only used when debug=false
            "handlers": ["console", "mail_admins"],
            "level": "ERROR",
            "propagate": True,
        },
    },
    # uncomment for django database query logs
    # 'loggers': {
    #     'django.db': {
    #         'level': 'DEBUG',
    #         'handlers': ['console'],
    #     }
    # }
}
