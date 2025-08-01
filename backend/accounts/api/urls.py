from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, OrganizationProfileViewSet, TrainerProfileViewSet, SelfTaskViewSet, ClientProfileViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')  # Register User viewset
router.register(r'organization', OrganizationProfileViewSet,
                basename='organization')  # Register OrganizationProfile viewset
router.register(r'trainer', TrainerProfileViewSet, basename='trainer')  # Register TrainerProfile viewset
router.register(r'selftasks', SelfTaskViewSet, basename='selftask')  # Register SelfTask viewset
router.register(r'client', ClientProfileViewSet, basename='client')  # Register ClientProfile viewset

urlpatterns = [
    path('', include(router.urls)),  # Include all router-generated URLs
]
