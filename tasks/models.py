from django.conf import settings
from django.db import models

from tasks.domain import TaskStatus
from tasks.domain.TaskStatus import STATUS_CHOICES, STATUS_NOT_STARTED


class Task(models.Model):
    title = models.CharField(max_length=256)
    status = models.IntegerField(choices=STATUS_CHOICES, default=STATUS_NOT_STARTED)
    description = models.TextField()

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def status_str(self):
        return TaskStatus.STATUS_CHOICES_DICT.get(self.status)

    def owner_id(self):
        if self.owner:
            return self.owner.id
        return None

    def __str__(self):
        return f'Task(title={self.title}, status={self.status}, description={self.description}' \
               f', owner={self.owner}, created_at={self.created_at}, updated_at={self.updated_at})'
