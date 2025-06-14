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
        
class DashboardStatsSerializer(serializers.Serializer):
    """
    Describes the dashboard stats
    """
    total_tasks = serializers.IntegerField(read_only=True)
    completed_tasks = serializers.IntegerField(read_only=True)
    pending_tasks = serializers.IntegerField(read_only=True)
    archived_tasks = serializers.IntegerField(read_only=True)
        
