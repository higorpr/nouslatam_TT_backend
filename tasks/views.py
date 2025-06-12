from rest_framework import viewsets
from .models import Task
from .serializers import TaskSerializer

class TaskViewSet(viewsets.ModelViewSet):
    
    
    serializer_class = TaskSerializer
    
    def get_queryset(self):
        """
        Filters the queryset to only return tasks for the current authorized
        user that is making the request
        """
        user = self.request.user
        
        # Verify if user is authorized
        if user.is_authenticated:
            return Task.objects.filter(owner=user).order_by('-created_at')
        else:
            return Task.objects.none()
        
    def perform_create(self,serializer):
        """
        This hook method injects the user into the task before it is saved
        """
        serializer.save(owner=self.request.user)
        
