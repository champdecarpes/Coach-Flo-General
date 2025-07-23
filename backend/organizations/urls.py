from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import OrganizationViewSet

# Create a router and register the OrganizationViewSet
router = DefaultRouter()
router.register(r'organizations', OrganizationViewSet, basename='organization')

# Include router URLs in the application
urlpatterns = [
    path('', include(router.urls)),
]
