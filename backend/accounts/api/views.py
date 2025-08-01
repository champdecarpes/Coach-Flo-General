from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from accounts.models import User, OrganizationProfile, TrainerProfile, SelfTask, ClientProfile
from accounts.api.serializers import UserSerializer, OrganizationProfileSerializer, TrainerProfileSerializer, \
    SelfTaskSerializer, ClientProfileSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    ViewSet for User model
    Handles CRUD operations for user authentication and profile data
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]


class OrganizationProfileViewSet(viewsets.ModelViewSet):
    """
    ViewSet for OrganizationProfile model
    Handles CRUD operations for organization profiles
    """
    queryset = OrganizationProfile.objects.all()
    serializer_class = OrganizationProfileSerializer
    permission_classes = [IsAuthenticated]


class TrainerProfileViewSet(viewsets.ModelViewSet):
    """
    ViewSet for TrainerProfile model
    Handles CRUD operations for trainer profiles
    """
    queryset = TrainerProfile.objects.all()
    serializer_class = TrainerProfileSerializer
    permission_classes = [IsAuthenticated]


class SelfTaskViewSet(viewsets.ModelViewSet):
    """
    ViewSet for SelfTask model
    Handles CRUD operations for trainer self-assigned tasks
    """
    queryset = SelfTask.objects.all()
    serializer_class = SelfTaskSerializer
    permission_classes = [IsAuthenticated]


class ClientProfileViewSet(viewsets.ModelViewSet):
    """
    ViewSet for ClientProfile model
    Handles CRUD operations for client profiles and related data
    """
    queryset = ClientProfile.objects.all()
    serializer_class = ClientProfileSerializer
    permission_classes = [IsAuthenticated]
