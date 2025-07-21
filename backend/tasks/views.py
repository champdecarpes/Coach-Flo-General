from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .models import Task
from .serializers import TaskSerializer


# ViewSet for Task model to handle CRUD operations
class TaskViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Task model.
    Provides CRUD operations: list, retrieve, create, update, partial_update, and delete.
    """
    # Queryset to fetch all Task objects
    queryset = Task.objects.all().select_related('body_metric')

    # Serializer class for Task model
    serializer_class = TaskSerializer

    permission_classes = [IsAuthenticated]
