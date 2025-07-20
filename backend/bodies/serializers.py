from rest_framework import serializers
from .models import Body, BodyChangeHistory


class BodyChangeHistorySerializer(serializers.ModelSerializer):
    """
    Serializer for BodyChangeHistory model
    """

    class Meta:
        model = BodyChangeHistory
        fields = '__all__'


class BodySerializer(serializers.ModelSerializer):
    """
    Serializer for Body model
    """

    class Meta:
        model = Body
        fields = '__all__'
