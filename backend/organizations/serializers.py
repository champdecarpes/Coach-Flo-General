from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Organization
from branding.serializers import BrandSerializer  # Assuming BrandSerializer exists


class OrganizationSerializer(serializers.ModelSerializer):
    """
    Serializer for the Organization model.
    Handles nested relationship with Brand and authentication fields.
    """
    branding = BrandSerializer(read_only=True)  # Read-only brand details
    password = serializers.CharField(write_only=True, required=False)  # Password field for authentication

    class Meta:
        model = Organization
        fields = '__all__'
        extra_kwargs = {
            'password': {'write_only': True},  # Ensure password is not returned in responses
        }

    def create(self, validated_data):
        """
        Create a new Organization instance with its Brand relationship.
        Expects an ID for branding.
        """
        User = get_user_model()
        branding_id = validated_data.pop('branding', None)
        password = validated_data.pop('password', None)

        # Create organization
        organization = User.objects.create_user(**validated_data)
        if password:
            organization.set_password(password)

        # Set branding relationship
        if branding_id:
            organization.branding_id = branding_id
            organization.save()

        return organization

    def update(self, instance, validated_data):
        """
        Update existing Organization instance and its Brand relationship.
        Updates organization fields and sets new branding ID.
        """
        User = get_user_model()
        branding_id = validated_data.pop('branding', None)
        password = validated_data.pop('password', None)

        # Update fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:
            instance.set_password(password)
        instance.save()

        # Update branding relationship
        if branding_id is not None:
            instance.branding_id = branding_id
            instance.save()

        return instance
