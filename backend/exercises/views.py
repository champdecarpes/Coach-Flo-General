from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from .models import Exercise, TrackingFields
from .serializers import ExerciseSerializer, TrackingFieldsSerializer

class ExerciseViewSet(viewsets.ModelViewSet):
    """
    ViewSet для управления упражнениями.
    Предоставляет CRUD-операции: list, create, retrieve, update, partial_update, destroy.
    Все поля модели, включая tracking_fields и monitored_fields, доступны для изменения через API.
    """
    queryset = Exercise.objects.all().select_related('tracking_fields')
    # select_related оптимизирует запросы для OneToOne связи
    serializer_class = ExerciseSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    # Разрешение: чтение для всех, запись только для аутентифицированных пользователей
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['modality', 'muscle_group', 'movement_pattern']
    # Фильтрация по полям modality, muscle_group, movement_pattern
    ordering_fields = ['id', 'modality', 'strength']
    # Сортировка по id, modality, strength

    def create(self, request, *args, **kwargs):
        """
        Создание нового упражнения.
        Выполняет валидацию и сохраняет данные, включая вложенный tracking_fields.
        Обрабатывает случай, если tracking_fields отсутствует в запросе.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            self.perform_create(serializer)
        except KeyError:
            # Если tracking_fields отсутствует, используем пустой объект
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
        Обновление существующего упражнения.
        Обновляет как сам объект Exercise, так и связанный tracking_fields.
        Поддерживает частичное обновление (PATCH).
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
    #     Кастомное действие для получения упражнений по модальности.
    #     Доступно по адресу /api/exercises/by-modality/<modality>/
    #     """
    #     exercises = self.queryset.filter(modality=modality)
    #     serializer = self.get_serializer(exercises, many=True)
    #     return Response(serializer.data)
