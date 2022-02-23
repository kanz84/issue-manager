from django.contrib.auth.models import User
from factory.django import DjangoModelFactory
from faker import Factory

from tasks.enums import TaskStatusEnum
from tasks.models import Task

faker = Factory.create()


class UserFactory(DjangoModelFactory):
    username = faker.name()
    email = faker.email()
    is_staff = True

    class Meta:
        model = User


class TaskFactory(DjangoModelFactory):
    def __init__(self, owner):
        self.owner = owner
    title = faker.word()
    status = TaskStatusEnum.NOT_STARTED
    description = faker.word()
    owner = None

    class Meta:
        model = Task


