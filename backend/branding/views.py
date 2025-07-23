from rest_framework import viewsets
from .models import Brand
from .serializers import BrandSerializer


class BrandViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing Brand instances.
    Supports all CRUD operations for brands.
    """
    queryset = Brand.objects.all()  # Retrieve all brands
    serializer_class = BrandSerializer  # Use BrandSerializer for data handling
