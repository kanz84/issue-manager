from rest_framework import serializers

from tasks.models import Task


class TaskSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.HiddenField(default=serializers.CurrentUserDefault())
    status_str = serializers.ReadOnlyField()

    owner_id = serializers.ReadOnlyField()

    class Meta:
        model = Task
        fields = ["id", "title", "status", "description", "status_str", "owner_id", "owner"]
