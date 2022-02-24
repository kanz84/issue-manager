import logging

from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets
from rest_framework.authentication import BasicAuthentication

from issuetracker.utils.authentication import CsrfExemptSessionAuthentication
from issuetracker.utils.util_views import IsOwner
from tasks.enums import TaskStatusEnum
from tasks.models import Task
from tasks.serializers import TaskSerializer

logger = logging.getLogger(__name__)


@method_decorator(csrf_exempt, name="dispatch")
class TaskModelViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.order_by("-id").all()
    serializer_class = TaskSerializer
    permission_classes = [IsOwner]
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(owner=self.request.user)


def task_detail_page(request, pk):
    return render(request, "tasks/task_detail.html", {"pk": pk, "status_choices_dict": TaskStatusEnum.to_dict()})


def task_list_page(request):
    return render(request, "tasks/task_list.html")


def task_create_page(request):
    return render(request, "tasks/task_detail.html", {"status_choices_dict": TaskStatusEnum.to_dict()})
