from django.conf import settings
from django.db import models

from tasks.enums import TaskStatusEnum


class Task(models.Model):
    title = models.CharField(max_length=256)
    status = models.CharField(
        choices=TaskStatusEnum.choices(),
        default=TaskStatusEnum.NOT_STARTED,
        max_length=2,
        help_text=TaskStatusEnum.help(),
    )
    description = models.TextField()

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def status_str(self):
        task_status = TaskStatusEnum.to_enum(self.status)
        return task_status.description if task_status else ""

    def owner_id(self):
        if self.owner:
            return self.owner.id
        return None

    def __str__(self):
        return f"Task(title={self.title})"
