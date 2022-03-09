import os

from django.contrib import admin
from django.urls import path, include
from django.views.static import serve

from issuetracker.settings import BASE_DIR

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

urlpatterns = [
    path(r"issue-mgr/", include(urlpatterns)),
]
