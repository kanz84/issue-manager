import os

from issuetracker.settings import DATABASES

DEBUG = False
ALLOWED_HOSTS = ["*"]
DATABASES["default"]["HOST"] = "issue_mgr_db"

STATIC_ROOT = "/workspace/files/static"
MEDIA_ROOT = "/workspace/files/media"

LOAD_STATICS = False

LOGGING_CONSOLE_LOG_LEVEL = "ERROR"
LOGGING_ENABLE_LOG_FILE_HANDLER = True


def ensure_get_file(path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    return path


LOGGING_FILE_LOCATION = ensure_get_file("/workspace/files/log/app.log")
