from rest_framework import serializers
from .models import Exercise, TrackingFields


class TrackingFieldsSerializer(serializers.ModelSerializer):
    """
    Serializer for the TrackingFields model
    Converts all model fields to JSON and back, including TimeField and DecimalField
    """

    class Meta:
        model = TrackingFields
        fields = '__all__'


class ExerciseSerializer(serializers.ModelSerializer):
    """
    Serializer for the Exercise model
    Handles all fields, including nested TrackingFields model via OneToOneField
    """
    tracking_fields = TrackingFieldsSerializer()

    class Meta:
        model = Exercise
        fields = '__all__'

    def validate_tracking_fields(self, value):
        """
        Validation for monitored_fields to ensure it contains no more than 3 elements
        """
        if value and len(value) > 3:
            raise serializers.ValidationError("No more than 3 tracking fields")
        return value

    def create(self, validated_data):
        """
        Create a new Exercise instance with nested TrackingFields model
        Extracts tracking_fields data, creates related object, and saves Exercise
        """
        # Handle case when tracking_fields might be empty
        tracking_data = validated_data.pop('tracking_fields', {})
        if tracking_data:
            tracking_instance = TrackingFields.objects.create(**tracking_data)
            exercise_instance = Exercise.objects.create(tracking_fields=tracking_instance, **validated_data)
        else:
            exercise_instance = Exercise.objects.create(**validated_data)
        return exercise_instance

    def update(self, instance, validated_data):
        """
        Update existing Exercise instance and related TrackingFields model
        Updates tracking_fields data and saves changes to both models
        """
        tracking_data = validated_data.pop('tracking_fields', {})

        if tracking_data and hasattr(instance, 'tracking_fields') and instance.tracking_fields:
            tracking_instance = instance.tracking_fields
            for attr, value in tracking_data.items():
                setattr(tracking_instance, attr, value)
            tracking_instance.save()
        elif tracking_data:
            # Create tracking_fields if it doesn't exist but data is provided
            tracking_instance = TrackingFields.objects.create(**tracking_data)
            instance.tracking_fields = tracking_instance

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance
