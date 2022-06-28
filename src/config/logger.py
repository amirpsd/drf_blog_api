from decouple import config
from os import path

from .settings import BASE_DIR

DEBUG = config("DEBUG", cast=bool, default=True)
min_level = "DEBUG" if DEBUG else "INFO"
min_django_level = "INFO"


LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "console":{
            "format": "{asctime} | {levelname} | {name} | {message}",
            "style": "{",
        },
        "verbose": {
            "format": "{asctime} | {levelname} | {name} | {module} | {process:d} | {thread:d} | {message}",
            "style": "{",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "console"
        },
        "file": {
            "level": min_level,
            "class": "logging.FileHandler",
            "filename": path.join(BASE_DIR, "log/app.log"),
            "formatter": "verbose",
        }
    },
    "loggers": {
        "": {
            "level": min_level,
            "handlers": ["file", "console",]
        }
    }
}
