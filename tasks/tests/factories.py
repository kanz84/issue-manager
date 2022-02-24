import factory
from django.contrib.auth.models import User
from factory import SubFactory
from factory.django import DjangoModelFactory
from faker import Factory

from tasks.enums import TaskStatusEnum
from tasks.models import Task

faker = Factory.create()


class UserFactory(DjangoModelFactory):
    username = factory.Sequence(lambda n: f"username_{n}")
    email = faker.email()
    is_staff = True

    class Meta:
        model = User


class TaskFactory(DjangoModelFactory):
    owner = SubFactory(UserFactory)
    title = faker.word()
    status = TaskStatusEnum.NOT_STARTED
    description = faker.word()

    class Meta:
        model = Task
