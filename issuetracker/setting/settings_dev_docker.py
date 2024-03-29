from issuetracker.settings import DATABASES

DEBUG = True
ALLOWED_HOSTS = ["*"]

LOGGING_FILE_LOCATION = "/workspace/files/log/app.log"
LOGGING_ENABLE_LOG_FILE_HANDLER = True
LOGGING_DB_BACKENDS_LOG_LEVEL = True

STATIC_ROOT = "/workspace/files/static"
MEDIA_ROOT = "/workspace/files/media"

DATABASES["default"]["HOST"] = "issue_mgr_db"
