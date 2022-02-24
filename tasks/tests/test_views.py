import logging

from django.test import TestCase
from django.urls import reverse
from rest_framework import status

from .factories import UserFactory, TaskFactory
from ..enums import TaskStatusEnum
from ..models import Task

logger = logging.getLogger(__name__)


class TaskViewSetTestCase(TestCase):
    def setUp(self):
        self.user = UserFactory(username="test", password="test", email="testuser@example.com", is_staff=True)
        self.user.set_password("test")
        self.user.save()

        result = self.client.login(
            password="test",
            username="test",
        )
        logger.info("login result is :%s", result)

    def test_get_list(self):
        owner = UserFactory()
        tasks = [TaskFactory(owner=owner) for i in range(0, 3)]

        list_url = reverse("tasks:task-list")
        logger.info("list_url is:%s", list_url)

        response = self.client.get(list_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(set(task["id"] for task in response.data), set(task.id for task in tasks))

    def test_retrieve(self):
        task = TaskFactory(owner=self.user)
        retrieve_url = reverse("tasks:task-retrieve", kwargs={"pk": task.id})
        response = self.client.get(retrieve_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], task.title)

    def test_update(self):
        task = TaskFactory(owner=self.user)
        update_url = reverse("tasks:task-update", kwargs={"pk": task.id})
        data = {"title": "New title", "description": "New description"}
        response = self.client.put(update_url, data=data, content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], data["title"])
        self.assertEqual(response.data["description"], data["description"])

    def test_create(self):
        self.assertEqual(Task.objects.count(), 0)
        create_url = reverse("tasks:task-create")
        data = {"title": "New title", "status": TaskStatusEnum.NOT_STARTED, "description": "New description"}

        user = UserFactory(
            username="test_su", password="test_su", email="test_suuser@example.com", is_staff=True, is_superuser=True
        )
        user.set_password("test_su")
        user.save()

        result = self.client.login(
            password="test_su",
            username="test_su",
        )
        logger.info("login result is :%s", result)

        response = self.client.post(create_url, data=data, content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["title"], data["title"])
        self.assertEqual(response.data["description"], data["description"])

    def test_delete(self):
        task = TaskFactory(owner=self.user)
        delete_url = reverse("tasks:task-delete", kwargs={"pk": task.id})
        response = self.client.delete(delete_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
