from django.db import models
from django.contrib.auth.models import User


class Task(models.Model):
    """
    Represents a task in the system
    """
    # Options for status field
    class Status(models.TextChoices):
        PENDING = "PENDING", "Pending"
        COMPLETED = "COMPLETED", "Completed"
        ARCHIVED = "ARCHIVED", "Archived"
    # Task title (name)
    title = models.CharField(
        max_length=200,
        verbose_name="Title",
    )
    # Task description (brief text)
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name="Description",
    )
    # Task status (can be expanded in the future, if needed)
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING,
        verbose_name="Status",
    )
    # Due date for task completion
    due_date = models.DateField(
        blank=True,
        null=True,
        verbose_name="Due Date",
    )
    # Task owner user
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,  # Associate User deletion to Task deletion
        related_name="tasks",
        verbose_name="Owner",
    )
    # Date and time task was created
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Created At",
    )
    # Date and time task was updated
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Updated At",
    )

    def __str__(self):
        """
        Returns a string representation of the object
        """
        return f'{self.title} ({self.get_status_display()})'  # type:ignore

    class Meta:
        ordering = ["due_date", "created_at"]
        verbose_name = "Task"
        verbose_name_plural = "Tasks"
