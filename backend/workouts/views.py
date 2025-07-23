from rest_framework import viewsets
from .models import Workout
from .serializers import WorkoutSerializer


class WorkoutViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing Workout instances.
    Supports CRUD operations with nested relationships to Sections, Exercises, and Trainer.
    """
    queryset = Workout.objects.all().prefetch_related('sections', 'exercises')  # Optimize related object queries
    serializer_class = WorkoutSerializer  # Use WorkoutSerializer for data handling

    def get_queryset(self):
        """
        Optionally restricts the returned workouts.
        Can be extended for filtering (e.g., by ownership or date).
        """
        return self.queryset
