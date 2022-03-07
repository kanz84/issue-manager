import logging
import os
import sys
import warnings
from pathlib import Path

from django.conf import settings


def get_log_file_location():
    log_file = settings.LOG_FILE_LOCATION
    if not os.path.exists(Path(log_file).resolve().parent):
        os.makedirs(Path(log_file).resolve().parent)
    return log_file


def is_in_run_mode():
    is_run_on_apache_ = len(sys.argv) > 0 and sys.argv[0] == "mod_wsgi"
    is_run_with_runserver = len(sys.argv) > 1 and sys.argv[1] == "runserver"
    is_run_with_gunicorn = len(sys.argv) > 0 and "gunicorn" in sys.argv[0]
    return is_run_on_apache_ or is_run_with_runserver or is_run_with_gunicorn


is_run_on_apache = len(sys.argv) > 0 and sys.argv[0] == "mod_wsgi"

warnings.simplefilter("default")
logging.captureWarnings(True)

LOGGING_CONFIGURATION = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "()": "colorlog.ColoredFormatter",
            "format": "{log_color}{asctime} [{levelname}] {name}.{funcName}({lineno}) rid({request_id}) "
            "pid({process:d}) {threadName}({thread:d})[{ip}] - {username} - {message}",
            "style": "{",
        },
        "simple": {
            "format": "{levelname} {message}",
            "style": "{",
        },
    },
    "filters": {
        "require_debug_true": {
            "()": "django.utils.log.RequireDebugTrue",
        },
        "require_debug_false": {
            "()": "django.utils.log.RequireDebugFalse",
        },
        "request_filter": {
            "()": "logger.RequestFilter",
        },
        "request_id_filter": {
            "()": "log_request_id.filters.RequestIDFilter",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "level": "ERROR" if is_run_on_apache else "DEBUG",
            "filters": ["request_filter", "request_id_filter"],
            # 'filters': ['require_debug_true'],
            "formatter": "verbose",
        },
        "file": {
            "class": "logging.handlers.TimedRotatingFileHandler",
            "level": "DEBUG",
            "filters": ["request_filter", "request_id_filter"],
            "formatter": "verbose",
            "filename": get_log_file_location(),
            "when": "midnight",
            "backupCount": 90,
        }
        if is_in_run_mode()
        else {"class": "logging.NullHandler"},
    },
    "root": {
        "handlers": ["console", "file"],
        "level": "INFO",
    },
    "loggers": {
        "": {
            "handlers": ["console", "file"],
            "level": "DEBUG",
            "propagate": False,
        },
        "django": {
            "handlers": ["console", "file"],
            "level": os.getenv("DJANGO_LOG_LEVEL", "INFO"),
            "propagate": False,
        },
        "django.request": {
            "handlers": ["console", "file"],
            "level": "DEBUG",
            "propagate": False,
        },
        "django.db.backends": {
            "handlers": ["console", "file"],
            "level": "INFO",
            "propagate": False,
        },
        "apscheduler.scheduler": {
            "level": "INFO",
            "handlers": ["console", "file"],
            "propagate": False,
        },
        "apscheduler": {
            "level": "WARN",
            "handlers": ["console", "file"],
            "propagate": False,
        },
        "mailer.engine": {
            "level": "WARN",
            "handlers": ["console", "file"],
            "propagate": False,
        },
        "django.db.backends.schema": {
            "level": "INFO" if settings.IS_TEST else "DEBUG",
            "handlers": ["console", "file"],
            "propagate": False,
        },
        "faker.factory": {
            "level": "INFO",
            "handlers": ["console", "file"],
            "propagate": False,
        },
        "factory": {
            "level": "INFO",
            "handlers": ["console", "file"],
            "propagate": False,
        },
    },
}


class RequestFilter(logging.Filter):
    def filter(self, record):
        user = record.request.user.username if hasattr(record, "request") and hasattr(record.request, "user") else None
        record.username = user if user else "system"
        ip = self.get_ip_address(record.request) if hasattr(record, "request") else None
        record.ip = ip if ip else "system"
        trace_id = (
            record.request.trace_id
            if hasattr(record, "request") and hasattr(record.request, "trace_id")
            else "NO_TRACE_ID"
        )
        record.trace_id = trace_id
        return True

    @staticmethod
    def get_ip_address(request):
        if not hasattr(request, "META"):
            return None
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR", None)
        return x_forwarded_for.split(",")[0] if x_forwarded_for else request.META.get("REMOTE_ADDR", None)
