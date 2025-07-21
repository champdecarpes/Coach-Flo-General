from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TaskViewSet

# Create a router for RESTful API routing
router = DefaultRouter()

# Register TaskViewSet with the prefix 'tasks'
router.register(r'tasks', TaskViewSet, basename='task')

# URL patterns for the tasks app
urlpatterns = [
    path('', include(router.urls)),  # Include all router-generated URLs
]
