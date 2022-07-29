from issuetracker.settings import DATABASES

DEBUG = False
ALLOWED_HOSTS = ["*"]
LOG_FILE_LOCATION = "/workspace/files/log/app.log"
DATABASES["default"]["HOST"] = "issue_mgr_db"

STATIC_ROOT = "/workspace/files/static"
MEDIA_ROOT = "/workspace/files/media"

LOAD_STATICS = False
