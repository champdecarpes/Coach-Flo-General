from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Client
from .serializers import ClientSerializer
from rest_framework.permissions import BasePermission


class IsOwnerOrReadOnly(BasePermission):
    """
    Custom permission to allow owners of an object to edit it.
    Read-only access is allowed for all authenticated users.
    """
    def has_object_permission(self, request, view, obj):
        # Allow read-only access for all authenticated users
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True
        # Allow full access only to the owner
        return obj == request.user


class ClientViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing Client instances.
    Supports CRUD operations with limited access to own data.
    """
    queryset = Client.objects.all().prefetch_related('exercises', 'workouts', 'programs').select_related('trainer', 'body_metrics')
    serializer_class = ClientSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def get_queryset(self):
        """
        Restrict the queryset to the authenticated user only.
        Ensures clients can only access their own data.
        """
        user = self.request.user
        if isinstance(user, Client):
            return self.queryset.filter(id=user.id)
        return self.queryset.none()
