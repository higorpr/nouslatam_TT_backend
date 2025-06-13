from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from django.urls import reverse
from .models import Task

User = get_user_model()


class TaskAPITests(APITestCase):
    """
    Task API tests
    """

    def setUp(self):
        """
        Build context for tests
        """
        # Create test user
        self.user = User.objects.create_user(  # type:ignore
            username='testuser_tasks',
            email='testuser@exemple.com',
            password='testpassword123',
        )
        # Authenticate user
        self.client.force_authenticate(user=self.user)
        # Create endopoint URL to be tested
        self.tasks_url = reverse('tasks:task-list')

    def test_create_task_successfully(self):
        """
        Test: Task should be successfully created by authenticated user
        """
        # Task data
        task_data = {
            'title': 'Task Creation Success Test',
            'description': 'Create test to ensure task creation is successful',
        }
        # Make request
        response = self.client.post(self.tasks_url, task_data, format='json')
        # Assert response status code
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # Assert number of tasks in DB
        self.assertEqual(Task.objects.count(), 1)
        # Assert test data
        task = Task.objects.get()
        self.assertEqual(task.title, task_data['title'])
        # Assert owner is created user
        self.assertEqual(task.owner, self.user)

    def test_unauthenticated_user_cannot_create_task(self):
        """
        Test: Unauthenticated user cannot create task
        """
        # Logout user
        self.client.logout()
        # Task data
        task_data = {
            'title': 'Task Creation Success Test',
            'description': 'Create test to ensure task creation is successful',
        }
        # Make request
        response = self.client.post(self.tasks_url, task_data, format='json')
        # Assert response status code
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        # Assert number of tasks in DB
        self.assertEqual(Task.objects.count(), 0)
