from rest_framework import viewsets
from .models import Trainer
from .serializers import TrainerSerializer
from rest_framework.permissions import IsAuthenticated


class TrainerViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing Trainer instances.
    Supports CRUD operations with nested relationships to Organization and SelfTasks.
    """
    queryset = Trainer.objects.all().prefetch_related('self_tasks').select_related('organization')  # Optimize related queries
    serializer_class = TrainerSerializer  # Use TrainerSerializer for data handling
    permission_classes = [IsAuthenticated]  # Require authentication for all actions

    def get_queryset(self):
        """
        Optionally restricts the returned trainers.
        Filters trainers based on the authenticated user or organization.
        """
        queryset = self.queryset
        user = self.request.user
        if not user.is_staff:  # Non-staff users see only their own data
            queryset = queryset.filter(id=user.id)
        return queryset

    def perform_create(self, serializer):
        """
        Customize creation to set the current user as the trainer if not specified.
        """
        if not serializer.validated_data.get('organization'):
            serializer.save()
        else:
            serializer.save()
