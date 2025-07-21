from rest_framework import serializers
from .models import Program
from workouts.serializers import WorkoutSerializer  # Assuming WorkoutSerializer exists
from sections.serializers import SectionSerializer  # Assuming SectionSerializer exists
from exercises.serializers import ExerciseSerializer  # Assuming ExerciseSerializer exists
from trainers.serializers import TrainerSerializer  # Assuming TrainerSerializer exists


class ProgramSerializer(serializers.ModelSerializer):
    """
    Serializer for the Program model.
    Handles nested relationships with Workouts, Sections, Exercises, and Trainer.
    """
    workouts = WorkoutSerializer(many=True, read_only=True)  # List of related workouts
    sections = SectionSerializer(many=True, read_only=True)  # List of related sections
    exercises = ExerciseSerializer(many=True, read_only=True)  # List of related exercises
    ownership = TrainerSerializer(read_only=True)  # Read-only trainer details
    created_at = serializers.DateTimeField(read_only=True)  # Read-only creation timestamp
    start_date = serializers.DateField(read_only=True)  # Read-only start date
    end_date = serializers.DateField(read_only=True)  # Read-only end date

    class Meta:
        model = Program
        fields = '__all__'

    def create(self, validated_data):
        """
        Create a new Program instance with nested relationships.
        Expects lists of workout, section, and exercise IDs.
        """
        workout_ids = validated_data.pop('workouts', [])
        section_ids = validated_data.pop('sections', [])
        exercise_ids = validated_data.pop('exercises', [])
        ownership_id = validated_data.pop('ownership', None)
        program_instance = Program.objects.create(**validated_data)
        if workout_ids:
            program_instance.workouts.set(workout_ids)
        if section_ids:
            program_instance.sections.set(section_ids)
        if exercise_ids:
            program_instance.exercises.set(exercise_ids)
        if ownership_id:
            program_instance.ownership_id = ownership_id
            program_instance.save()
        return program_instance

    def update(self, instance, validated_data):
        """
        Update existing Program instance and its relationships.
        Updates program fields and sets new relationship IDs.
        """
        workout_ids = validated_data.pop('workouts', [])
        section_ids = validated_data.pop('sections', [])
        exercise_ids = validated_data.pop('exercises', [])
        ownership_id = validated_data.pop('ownership', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        if workout_ids:
            instance.workouts.set(workout_ids)
        if section_ids:
            instance.sections.set(section_ids)
        if exercise_ids:
            instance.exercises.set(exercise_ids)
        if ownership_id is not None:
            instance.ownership_id = ownership_id
            instance.save()
        return instance
