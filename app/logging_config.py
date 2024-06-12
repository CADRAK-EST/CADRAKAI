import logging
import logging.config
import os

# Define the logging configuration
LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "standard": {
            "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        }
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "standard",
            "level": "INFO",
            "stream": "ext://sys.stdout"
        },
        "file_handler": {
            "class": "logging.FileHandler",
            "formatter": "standard",
            "level": "DEBUG",
            "filename": "logs/app.log",
            "mode": "a",
            "encoding": "utf-8"
        }
    },
    "loggers": {
        "": {
            "handlers": ["console", "file_handler"],
            "level": "DEBUG",
            "propagate": True
        }
    }
}

def setup_logging():
    if not os.path.exists('logs'):
        os.makedirs('logs')
    logging.config.dictConfig(LOGGING_CONFIG)
