from rest_framework import viewsets
from .models import Task
from .serializers import TaskSerializer, DashboardStatsSerializer
from rest_framework.views import APIView
from django.db.models import Count, Q
from rest_framework import permissions, status
from drf_spectacular.utils import extend_schema
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter


class TaskViewSet(viewsets.ModelViewSet):

    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    filter_backends = [DjangoFilterBackend, SearchFilter]

    # Exact filter fields
    filterset_fields = ['status']

    # Text filter fields
    search_fields = ['title', 'description']

    def get_queryset(self):
        """
        Filters the queryset to only return tasks for the current authorized
        user that is making the request
        """
        user = self.request.user

        # Verify if user is authorized
        if user.is_authenticated:
            return Task.objects.filter(owner=user).order_by('-created_at')

    def perform_create(self, serializer):
        """
        This hook method injects the user into the task before it is saved
        """
        serializer.save(owner=self.request.user)


class DashboardStatsView(APIView):
    """
    Returns dashboard stats for logged user
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = DashboardStatsSerializer

    @extend_schema(
        summary="Returns dashboard stats for logged user",
        description="Returns total task count and task counts based on status",
        responses={200: DashboardStatsSerializer},)
    def get(self, request, *ags, **kwargs):
        user = request.user

        stats = Task.objects.filter(owner=user).aggregate(
            total_tasks=Count('id'),
            completed_tasks=Count('id', filter=Q(status='COMPLETED')),
            pending_tasks=Count('id', filter=Q(status='PENDING')),
            archived_tasks=Count('id', filter=Q(status='ARCHIVED')),
        )

        return Response(data=stats, status=status.HTTP_200_OK)
