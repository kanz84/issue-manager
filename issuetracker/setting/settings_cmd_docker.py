from issuetracker.settings import DATABASES

DEBUG = False
ALLOWED_HOSTS = ["*"]

DATABASES["default"]["HOST"] = "issue_mgr_db"

LOGGING_ENABLE_LOG_FILE_HANDLER = False
LOGGING_DB_BACKENDS_SCHEMA_LOG_LEVEL = "INFO"
