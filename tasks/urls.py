from django.urls import path, re_path, include
from rest_framework.routers import DefaultRouter

from tasks import views

app_name = "tasks"

router = DefaultRouter()
router.register(r"tasks", views.TaskModelViewSet, basename="task")


urlpatterns = [
    path("", views.task_list_page, name="task_list_page"),
    re_path("", include(router.urls)),
    path("task/page/detail/<int:pk>", views.task_detail_page, name="task_detail"),
    path("task/page/create/", views.task_create_page, name="task_create_page"),
]
