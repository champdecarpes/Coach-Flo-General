from rest_framework import serializers
from .models import Brand


class BrandSerializer(serializers.ModelSerializer):
    """
    Serializer for the Brand model.
    Handles basic fields for brand creation and updates.
    """
    class Meta:
        model = Brand
        fields = '__all__'
