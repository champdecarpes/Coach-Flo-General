from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TrainerViewSet

# Create a router and register the TrainerViewSet
router = DefaultRouter()
router.register(r'trainers', TrainerViewSet, basename='trainer')

# Include router URLs in the application
urlpatterns = [
    path('', include(router.urls)),
]
