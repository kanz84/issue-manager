from django.contrib.auth.models import User
from factory import SubFactory
from factory.django import DjangoModelFactory
from faker import Factory

from tasks.domain import TaskStatus
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
    status = TaskStatus.STATUS_NOT_STARTED
    description = faker.word()
    owner = None

    class Meta:
        model = Task


