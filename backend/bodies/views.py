from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import BodyChangeHistory
from .serializers import BodyChangeHistorySerializer


class BodyChangeHistoryViewSet(viewsets.ModelViewSet):
    """
    Handles Read, Update, and Delete operations
    """
    queryset = BodyChangeHistory.objects.all()
    serializer_class = BodyChangeHistorySerializer
    permission_classes = [IsAuthenticated]  # Restrict access to authenticated users

    def get_permissions(self):
        """
        Defines permissions based on action
        Read-only for all authenticated users, Update and Delete require additional checks
        """
        if self.action in ['update', 'partial_update', 'destroy']:
            self.permission_classes = [IsAuthenticated]  # Can add more restrictive permissions here
        return super().get_permissions()

    def create(self, request, *args, **kwargs):
        """
        Disables Create operation
        Returns 405 Method Not Allowed
        """
        return Response(status=405)
