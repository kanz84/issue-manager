import logging
from django.test import TestCase
from .factories import TaskFactory

from ..serializers import TaskSerializer

logger = logging.getLogger(__name__)


class TaskSerializerTest(TestCase):
    def test_model_fields(self):
        task = TaskFactory()

        logger.info(task)

        serializer = TaskSerializer(task)

        for field_name in ['title', 'description', 'status']:
            self.assertEqual(serializer.data[field_name], getattr(task, field_name))