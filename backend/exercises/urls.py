from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ExerciseViewSet

router = DefaultRouter()
router.register(r'exercises', ExerciseViewSet, basename='exercise')
# Регистрирует маршруты для ExerciseViewSet
# Создает эндпоинты: /api/exercises/ (список/создание), /api/exercises/{id}/ (детали/обновление/удаление)
# basename обеспечивает уникальные имена для маршрутов

urlpatterns = [
    path('api/', include(router.urls)),
    # Подключает маршруты API с префиксом /api/
    # Примеры эндпоинтов: /api/exercises/, /api/exercises/1/, /api/exercises/by-modality/cardio/
]
