DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
    }
}

LOGGING_ENABLE_LOG_FILE_HANDLER = False
LOGGING_DB_BACKENDS_SCHEMA_LOG_LEVEL = "INFO"
