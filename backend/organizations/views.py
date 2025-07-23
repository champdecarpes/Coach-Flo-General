from rest_framework import viewsets
from .models import Organization
from .serializers import OrganizationSerializer


class OrganizationViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing Organization instances.
    Supports CRUD operations with nested relationship to Brand.
    """
    queryset = Organization.objects.all().select_related('branding')  # Optimize Brand relationship query
    serializer_class = OrganizationSerializer  # Use OrganizationSerializer for data handling

    def get_queryset(self):
        """
        Optionally restricts the returned organizations.
        Can be extended for filtering (e.g., by user or branding).
        """
        return self.queryset
