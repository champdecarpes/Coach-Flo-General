from rest_framework import serializers
from .models import Section
from exercises.serializers import ExerciseSerializer  # Assuming ExerciseSerializer exists


class SectionSerializer(serializers.ModelSerializer):
    """
    Serializer for the Section model.
    Handles nested Exercise relationships and section-specific settings.
    """
    exercises = ExerciseSerializer(many=True, read_only=True)  # List of related exercises
    created_at = serializers.DateTimeField(read_only=True)  # Read-only creation timestamp

    class Meta:
        model = Section
        fields = '__all__'

    def create(self, validated_data):
        """
        Create a new Section instance with nested Exercise relationships.
        Expects a list of exercise IDs in the 'exercises' field.
        """
        exercise_ids = validated_data.pop('exercises', [])
        section_instance = Section.objects.create(**validated_data)
        if exercise_ids:
            section_instance.exercises.set(exercise_ids)
        return section_instance

    def update(self, instance, validated_data):
        """
        Update existing Section instance and its Exercise relationships.
        Updates section fields and sets new exercise IDs.
        """
        exercise_ids = validated_data.pop('exercises', [])
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        if exercise_ids:
            instance.exercises.set(exercise_ids)
        return instance
