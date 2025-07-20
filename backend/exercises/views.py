from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from .models import Exercise, TrackingFields
from .serializers import ExerciseSerializer, TrackingFieldsSerializer


class ExerciseViewSet(viewsets.ModelViewSet):
    """
    CRUD: list, create, retrieve, update, partial_update, destroy
    All model fields are available for modification via API
    """
    queryset = Exercise.objects.all().select_related('tracking_fields')

    # select_related optimizes queries for OneToOne relationship
    serializer_class = ExerciseSerializer
    # Read access for all, write access only for authenticated users

    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]

    # Filtering by modality, muscle_group, movement_pattern fields
    search_fields = ['modality', 'muscle_group', 'movement_pattern']
    # Sorting by id, modality, strength
    ordering_fields = ['id', 'modality', 'strength']

    def create(self, request, *args, **kwargs):
        """
        Create new Exercise object
        Performs validation and saves data including nested tracking_fields
        Handles case when tracking_fields is missing in request
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            self.perform_create(serializer)
        except KeyError:
            # If tracking_fields is missing, use empty object
            tracking_data = {'time': '00:00:00', 'speed': 0.00, 'cadence': 0.000, 'distance': 0.00,
                             'reps': 0, 'weight': 0.00, 'heart_rate': 0.00, 'percentage_hr': 0.000,
                             'rpm': 0.00, 'round_field': 0, 'rest': '00:00:00'}
            validated_data = serializer.validated_data
            validated_data['tracking_fields'] = tracking_data
            serializer = self.get_serializer(data=validated_data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=201, headers=headers)

    def update(self, request, *args, **kwargs):
        """
        Update existing Exercise object
        Supports PATCH
        """
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    # @action(detail=False, methods=['get'], url_path='by-modality/(?P<modality>\w+)')
    # def by_modality(self, request, modality=None):
    #     """
    #     Custom action to get Exercise objects by modality
    #     Available at /api/exercises/by-modality/<modality>/
    #     """
    #     exercises = self.queryset.filter(modality=modality)
    #     serializer = self.get_serializer(exercises, many=True)
    #     return Response(serializer.data)
