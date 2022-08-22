import logging
import os

from django.conf import settings
from django.contrib import admin
from django.urls import path, include, re_path
from django.views.static import serve

from issuetracker.settings import BASE_DIR

logger = logging.getLogger(__name__)

logger.info("System is starting with [env=%s, db=%s]", settings.ENV, settings.DATABASES["default"]["ENGINE"])

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("django.contrib.auth.urls")),
    path("api-auth/", include("rest_framework.urls")),
    path("", include("tasks.urls")),
]

urlpatterns += [
    path(
        "favicon.ico",
        serve,
        {
            "path": "favicon.ico",
            "document_root": os.path.join(BASE_DIR, "tasks/static"),
        },
    ),
]
if settings.LOAD_STATICS:
    urlpatterns += [re_path(r"^static/(?P<path>.*)$", serve, {"document_root": settings.STATIC_ROOT})]

urlpatterns = [
    path(r"issue-mgr/", include(urlpatterns)),
]
