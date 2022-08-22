from issuetracker.settings import DATABASES

DEBUG = True
ALLOWED_HOSTS = ["*"]

DATABASES["default"]["HOST"] = "issue_mgr_db"
