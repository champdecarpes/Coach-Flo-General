from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import WorkoutViewSet

# Create a router and register the WorkoutViewSet
router = DefaultRouter()
router.register(r'workouts', WorkoutViewSet, basename='workout')

# Include router URLs in the application
urlpatterns = [
    path('', include(router.urls)),
]
