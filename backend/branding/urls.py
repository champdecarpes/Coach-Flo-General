from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BrandViewSet

# Create a router and register the BrandViewSet
router = DefaultRouter()
router.register(r'brands', BrandViewSet, basename='brand')

# Include router URLs in the application
urlpatterns = [
    path('', include(router.urls)),
]
