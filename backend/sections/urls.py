from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SectionViewSet

# Create a router and register the SectionViewSet
router = DefaultRouter()
router.register(r'sections', SectionViewSet, basename='section')

# Include router URLs in the application
urlpatterns = [
    path('', include(router.urls)),
]
