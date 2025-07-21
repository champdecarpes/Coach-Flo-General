from rest_framework import viewsets
from .models import Section
from .serializers import SectionSerializer


class SectionViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing Section instances
    Supports CRUD operations with nested Exercise relationships
    """
    queryset = Section.objects.all().prefetch_related('exercises')  # Optimize related object queries
    serializer_class = SectionSerializer  # Use SectionSerializer for data handling

    def get_queryset(self):
        """
        Optionally restricts the returned sections
        Can be extended for filtering (e.g., by user or date)
        """
        return self.queryset
