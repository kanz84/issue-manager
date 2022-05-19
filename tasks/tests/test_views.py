from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from tasks.enums import TaskStatusEnum
from tasks.models import Task
from tasks.tests.factories import UserFactory, TaskFactory

# reload ...

class TaskViewSetTestCase(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = user = UserFactory()
        cls.user_other = user_other = UserFactory()

        cls.task = TaskFactory(owner=user)
        TaskFactory(owner=user)
        TaskFactory(owner=user)
        cls.task_other = TaskFactory(owner=user_other)

    def setUp(self):
        self.client.force_authenticate(user=self.user)

    def test_list(self):

        res = self.client.get(reverse("tasks:task-list"))
        self.assertEqual(status.HTTP_200_OK, res.status_code)

        res_data = {task["id"]: task for task in res.data}
        self.assertEqual(3, len(res_data))
        self.assertEqual(res_data.keys(), {task.id for task in Task.objects.filter(owner=self.user).all()})

        # validate schema ...
        res_data1 = res_data[self.task.id]
        self.assertEqual(self.task.title, res_data1["title"])
        self.assertEqual(self.task.status, res_data1["status"])
        self.assertEqual(self.task.description, res_data1["description"])
        self.assertEqual(self.task.status_str(), res_data1["status_str"])
        self.assertEqual(self.task.owner.id, res_data1["owner_id"])

    def test_retrieve(self):
        res = self.client.get(reverse("tasks:task-detail", kwargs={"pk": self.task.id}))
        self.assertEqual(status.HTTP_200_OK, res.status_code)

        self.assertEqual(self.task.id, res.data["id"])
        self.assertEqual(self.task.title, res.data["title"])
        self.assertEqual(self.task.status, res.data["status"])
        self.assertEqual(self.task.description, res.data["description"])
        self.assertEqual(self.task.status_str(), res.data["status_str"])
        self.assertEqual(self.task.owner.id, res.data["owner_id"])

    def test_retrieve_wrong_owner(self):
        res = self.client.get(reverse("tasks:task-detail", kwargs={"pk": self.task_other.id}))
        self.assertEqual(status.HTTP_404_NOT_FOUND, res.status_code)

    def test_update(self):
        task = TaskFactory(owner=self.user)
        data = {"title": "New title", "description": "New description"}
        res = self.client.put(reverse("tasks:task-detail", kwargs={"pk": task.id}), data=data)
        self.assertEqual(status.HTTP_200_OK, res.status_code)

        self.assertEqual(data["title"], res.data["title"])
        self.assertEqual(data["description"], res.data["description"])

        task_ = Task.objects.get(pk=task.id)

        self.assertEqual(data["title"], task_.title)
        self.assertEqual(data["description"], task_.description)

    def test_update_wrong_owner(self):
        res = self.client.put(reverse("tasks:task-detail", kwargs={"pk": self.task_other.id}), data={})
        self.assertEqual(status.HTTP_404_NOT_FOUND, res.status_code)

    def test_create(self):
        data = {
            "title": "New title",
            "status": TaskStatusEnum.NOT_STARTED,
            "description": "New description",
        }

        res = self.client.post(reverse("tasks:task-list"), data=data)
        self.assertEqual(status.HTTP_201_CREATED, res.status_code)

        self.assertEqual(data["title"], res.data["title"])
        self.assertEqual(data["description"], res.data["description"])

        task_ = Task.objects.get(pk=res.data["id"])

        self.assertEqual(data["title"], task_.title)
        self.assertEqual(data["description"], task_.description)
        self.assertEqual(self.user.id, task_.owner.id)

    def test_create_required_fields(self):
        res = self.client.post(reverse("tasks:task-list"), data={})
        self.assertEqual(status.HTTP_400_BAD_REQUEST, res.status_code)

        self.assertEqual("required", res.data["title"][0].code)
        self.assertEqual("required", res.data["description"][0].code)

    def test_delete(self):
        task = TaskFactory(owner=self.user)
        res = self.client.delete(reverse("tasks:task-detail", kwargs={"pk": task.id}))
        self.assertEqual(status.HTTP_204_NO_CONTENT, res.status_code)

        self.assertFalse(Task.objects.filter(pk=task.id).exists())

    def test_delete_wrong_owner(self):
        res = self.client.delete(reverse("tasks:task-detail", kwargs={"pk": self.task_other.id}))
        self.assertEqual(status.HTTP_404_NOT_FOUND, res.status_code)
