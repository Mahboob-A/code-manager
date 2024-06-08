from .base import *  # noqa
from .base import env  # noqa: E501

# warnigns for linters code - E501 for unused variables


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env(
    "DJANGO_SECRET_KEY",
    default="django-insecure-!c=ip7oq+2mojk#6bg#whq45!05+t^^5&6$q4c87!5eg8p2for",
)

DEBUG = True

CSRF_TRUSTED_ORIGINS = [
    "http://localhost:8000",
    "http://127.0.0.1:8000",
    "http://127.0.0.1:8080",
]

ALLOWED_HOSTS = ["127.0.0.1"]


# Time to cache the code execution result in redis
REDIS_CACHE_TIME_IN_SECONDS = int(env("REDIS_CACHE_TIME_IN_SECONDS"))

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
MONGO_DB_NAME = env("MONGO_INITDB_DATABASE",)
MONGO_USER = env("MONGO_INITDB_ROOT_USERNAME")
MONGO_PASS = env("MONGO_INITDB_ROOT_PASSWORD")
MONGO_RESULT_COLLECTIOIN = env("MONGO_INITDB_COLLECTION")
MONGO_AUTH_SOURCE_DB = env("MONGO_AUTH_SOURCE_DB")


# AWS is Discarded.
# AWS_ACCESS_KEY_ID = env("AWS_ACCESS_KEY_ID")
# AWS_SECRET_ACCESS_KEY = env("AWS_SECRET_ACCESS_KEY")
# AWS_STORAGE_BUCKET_NAME = env("AWS_STORAGE_BUCKET_NAME")
# AWS_DEFAULT_ACL = "public-read"
# AWS_S3_CUSTOM_DOMAIN = f"{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com"
# AWS_S3_OBJECT_PARAMETERS = {
#     "CacheControl": "max-age=86400",
# }
# AWS_LOCATION = env("AWS_LOCATION")


# logging
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "%(levelname)s %(name)-12s %(asctime)s %(module)s  %(process)d %(thread)d %(message)s "
        }
    },
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        }
    },
    "root": {
        "level": "INFO",
        "handlers": ["console"],
    },
    # uncomment for django database query logs
    # "loggers": {
    #     "django.db": {
    #         "level": "DEBUG",
    #         "handlers": ["console"],
    #     }
    # },
}
