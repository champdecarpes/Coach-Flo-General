from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ClientViewSet

# Create a router and register the ClientViewSet
router = DefaultRouter()
router.register(r'clients', ClientViewSet, basename='client')

# Include router URLs in the application
urlpatterns = [
    path('', include(router.urls)),
]
