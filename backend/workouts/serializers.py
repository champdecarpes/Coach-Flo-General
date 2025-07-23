from rest_framework import serializers
from .models import Workout
from sections.serializers import SectionSerializer  # Assuming SectionSerializer exists
from exercises.serializers import ExerciseSerializer  # Assuming ExerciseSerializer exists
from trainers.serializers import TrainerSerializer  # Assuming TrainerSerializer exists


class WorkoutSerializer(serializers.ModelSerializer):
    """
    Serializer for the Workout model
    Handles nested relationships with Sections, Exercises, and Trainer
    """
    sections = SectionSerializer(many=True, read_only=True)  # List of related sections
    exercises = ExerciseSerializer(many=True, read_only=True)  # List of related exercises
    ownership = TrainerSerializer(read_only=True)  # Read-only trainer details
    created_at = serializers.DateTimeField(read_only=True)  # Read-only creation timestamp

    class Meta:
        model = Workout
        fields = '__all__'

    def create(self, validated_data):
        """
        Create a new Workout instance with nested relationships
        Expects lists of section and exercise IDs
        """
        section_ids = validated_data.pop('sections', [])
        exercise_ids = validated_data.pop('exercises', [])
        ownership_id = validated_data.pop('ownership', None)
        workout_instance = Workout.objects.create(**validated_data)
        if section_ids:
            workout_instance.sections.set(section_ids)
        if exercise_ids:
            workout_instance.exercises.set(exercise_ids)
        if ownership_id:
            workout_instance.ownership_id = ownership_id
            workout_instance.save()
        return workout_instance

    def update(self, instance, validated_data):
        """
        Update existing Workout instance and its relationships
        Updates workouts fields and sets new relationship IDs
        """
        section_ids = validated_data.pop('sections', [])
        exercise_ids = validated_data.pop('exercises', [])
        ownership_id = validated_data.pop('ownership', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        if section_ids:
            instance.sections.set(section_ids)
        if exercise_ids:
            instance.exercises.set(exercise_ids)
        if ownership_id is not None:
            instance.ownership_id = ownership_id
            instance.save()
        return instance
