from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProgramViewSet

# Create a router and register the ProgramViewSet
router = DefaultRouter()
router.register(r'programs', ProgramViewSet, basename='program')

# Include router URLs in the application
urlpatterns = [
    path('', include(router.urls)),
]
