import logging

from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.mixins import (CreateModelMixin, ListModelMixin, RetrieveModelMixin, UpdateModelMixin,
                                   DestroyModelMixin)
from rest_framework.permissions import IsAuthenticated, AllowAny, DjangoModelPermissionsOrAnonReadOnly
from rest_framework.viewsets import GenericViewSet

from tasks.domain.CsrfExempt import CsrfExemptSessionAuthentication
from tasks.domain.Owner import IsOwner
from tasks.domain import TaskStatus
from tasks.models import Task
from tasks.serializers import TaskSerializer

logger = logging.getLogger(__name__)


@method_decorator(csrf_exempt, name='dispatch')
class TaskRetrieveUpdateDeleteViewSet(GenericViewSet, RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin):
    queryset = Task.objects.all().order_by('-id')
    serializer_class = TaskSerializer
    permission_classes = [IsOwner]
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)


@method_decorator(csrf_exempt, name='dispatch')
class TaskListCreateViewSet(GenericViewSet, CreateModelMixin, ListModelMixin):
    queryset = Task.objects.all().order_by('-id')
    serializer_class = TaskSerializer
    permission_classes = [DjangoModelPermissionsOrAnonReadOnly]
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


def task_detail_page(request, pk):
    return render(request, 'tasks/task_detail.html', {
        'pk': pk,
        'status_choices_dict': TaskStatus.STATUS_CHOICES_DICT
    })


def task_list_page(request):
    return render(request, 'tasks/task_list.html')


def task_create_page(request):
    return render(request, 'tasks/task_detail.html', {
        'status_choices_dict': TaskStatus.STATUS_CHOICES_DICT
    })