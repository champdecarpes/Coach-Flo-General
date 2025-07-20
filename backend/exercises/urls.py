from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ExerciseViewSet

router = DefaultRouter()
router.register(r'exercises', ExerciseViewSet, basename='exercise')
# Registers routes for ExerciseViewSet
# Endpoints: /api/exercises/ (read/create), /api/exercises/{id}/ (update/delete)
# basename ensures unique route names

urlpatterns = [
    path('api/', include(router.urls)),
    # Connects API routes with /api/ prefix
    # Examples of endpoints: /api/exercises/, /api/exercises/1/, /api/exercises/by-modality/cardio/
]
