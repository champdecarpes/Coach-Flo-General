from rest_framework import serializers
from .models import Exercise, TrackingFields


class TrackingFieldsSerializer(serializers.ModelSerializer):
    """
    Serializer for the TrackingFields model.
    Handles individual tracking data for an exercise.
    """
    class Meta:
        model = TrackingFields
        fields = '__all__'


class ExerciseSerializer(serializers.ModelSerializer):
    """
    Serializer for the Exercise model.
    Handles multiple TrackingFields as a nested list.
    """
    tracking_fields = TrackingFieldsSerializer(many=True, read_only=True)  # List of tracking fields

    class Meta:
        model = Exercise
        fields = '__all__'

    def validate_monitored_fields(self, value):
        """
        Validate monitored_fields to ensure it contains no more than 3 elements.
        """
        if value and len(value) > 3:
            raise serializers.ValidationError("No more than 3 tracking fields")
        return value

    def create(self, validated_data):
        """
        Create a new Exercise instance with nested TrackingFields.
        Expects a list of tracking_fields data in the request.
        """
        tracking_data = validated_data.pop('tracking_fields', [])
        exercise_instance = Exercise.objects.create(**validated_data)
        if tracking_data:
            for track_data in tracking_data:
                TrackingFields.objects.create(exercise=exercise_instance, **track_data)
        return exercise_instance

    def update(self, instance, validated_data):
        """
        Update existing Exercise instance and related TrackingFields.
        Updates or creates TrackingFields based on provided data.
        """
        tracking_data = validated_data.pop('tracking_fields', [])
        # Update existing fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # Update or create TrackingFields
        if tracking_data:
            # Delete existing tracking fields to avoid duplication (custom logic can be adjusted)
            instance.tracking_fields.all().delete()
            for track_data in tracking_data:
                TrackingFields.objects.create(exercise=instance, **track_data)

        return instance
