from rest_framework import viewsets
from .models import Program
from .serializers import ProgramSerializer


class ProgramViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing Program instances
    Supports CRUD operations with nested relationships to Workouts, Sections, Exercises, and Trainer
    """
    queryset = Program.objects.all().prefetch_related('workouts', 'sections', 'exercises')  # Optimize related object queries
    serializer_class = ProgramSerializer  # Use ProgramSerializer for data handling

    def get_queryset(self):
        """
        Optionally restricts the returned programs
        Can be extended for filtering (e.g., by ownership or date)
        """
        return self.queryset
