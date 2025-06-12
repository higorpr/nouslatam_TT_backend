from rest_framework import serializers
from .models import Task


class TaskSerializer(serializers.ModelSerializer):
    """
    Serializer for the Task model
    """
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Task
        fields = ('id', 'title', 'description', 'status',
                  'due_date', 'created_at', 'updated_at', 'owner')
        read_only_fields = ['created_at', 'updated_at']
