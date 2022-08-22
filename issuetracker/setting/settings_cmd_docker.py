from issuetracker.settings import DATABASES

DEBUG = False
ALLOWED_HOSTS = ["*"]

DATABASES["default"]["HOST"] = "issue_mgr_db"
