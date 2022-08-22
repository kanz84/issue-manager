import logging
import os
import warnings

from django.conf import settings

warnings.simplefilter("default")
logging.captureWarnings(True)


LOGGING_CONFIGURATION = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "()": "colorlog.ColoredFormatter",
            "format": "{log_color}{asctime} [{levelname}] {name}.{funcName}({lineno}) req_id({request_id}) "
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
            "level": settings.LOGGING_CONSOLE_LOG_LEVEL,
            "filters": ["request_filter", "request_id_filter"],
            # 'filters': ['require_debug_true'],
            "formatter": "verbose",
        },
        "file": {
            "class": "logging.handlers.TimedRotatingFileHandler",
            "level": "DEBUG",
            "filters": ["request_filter", "request_id_filter"],
            "formatter": "verbose",
            "filename": settings.LOGGING_FILE_LOCATION,
            "when": "midnight",
            "backupCount": 36500,
        }
        if settings.LOGGING_ENABLE_LOG_FILE_HANDLER
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
            "level": settings.LOGGING_DB_BACKENDS_LOG_LEVEL,
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
            "level": settings.LOGGING_DB_BACKENDS_SCHEMA_LOG_LEVEL,
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
        "gunicorn.error": {
            "level": "DEBUG",
            "handlers": ["console", "file"],
            "propagate": False,
        },
    },
}


def configure_my_logging(_=None):
    import logging.config  # pylint: disable=redefined-outer-name

    logging.config.dictConfig(LOGGING_CONFIGURATION)


def get_ip_address(request):
    if not request:
        return None
    if not hasattr(request, "META"):
        return None
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR", None)
    return x_forwarded_for.split(",")[0] if x_forwarded_for else request.META.get("REMOTE_ADDR", None)


class RequestFilter(logging.Filter):
    def filter(self, record):
        user = record.request.user.username if hasattr(record, "request") and hasattr(record.request, "user") else None
        record.username = user if user else "system"
        ip = get_ip_address(record.request) if hasattr(record, "request") else None
        record.ip = ip if ip else "system"
        trace_id = (
            record.request.trace_id
            if hasattr(record, "request") and hasattr(record.request, "trace_id")
            else "NO_TRACE_ID"
        )
        record.trace_id = trace_id
        return True
