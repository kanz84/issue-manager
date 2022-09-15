from issuetracker.settings import DATABASES

DEBUG = False
ALLOWED_HOSTS = ["*"]
DATABASES["default"]["HOST"] = "issue_mgr_db"

STATIC_ROOT = "/workspace/files/static"
MEDIA_ROOT = "/workspace/files/media"

LOAD_STATICS = False
LOGGING_DB_BACKENDS_SCHEMA_LOG_LEVEL = "INFO"
LOGGING_ENABLE_LOG_FILE_HANDLER = False
