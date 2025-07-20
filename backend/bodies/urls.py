from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BodyChangeHistoryViewSet

router = DefaultRouter()
router.register(r'bodychangehistory', BodyChangeHistoryViewSet,
                basename='bodychangehistory')  # Register viewset for history

urlpatterns = [
    path('api/', include(router.urls)),  # Include API routes with /api/ prefix
]
