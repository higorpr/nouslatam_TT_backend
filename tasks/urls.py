from django.urls import path, include, re_path
from rest_framework.routers import DefaultRouter
from .views import TaskViewSet, DashboardStatsView

app_name = 'tasks'

router = DefaultRouter(trailing_slash=False)
router.register(r'', TaskViewSet, basename='task')

urlpatterns = [
    re_path(r'^dashboard/?$', DashboardStatsView.as_view(),
         name='dashboard-stats'),  # Dashboard route
    path('', include(router.urls))  # All basic task CRUD
]
