from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Client
from trainers.serializers import TrainerSerializer  # Assuming TrainerSerializer exists
from bodies.serializers import BodySerializer  # Assuming BodySerializer exists
from exercises.serializers import ExerciseSerializer  # Assuming ExerciseSerializer exists
from workouts.serializers import WorkoutSerializer  # Assuming WorkoutSerializer exists
from programs.serializers import ProgramSerializer  # Assuming ProgramSerializer exists


class ClientSerializer(serializers.ModelSerializer):
    """
    Serializer for the Client model.
    Handles nested relationships with Trainer, Body, Exercises, Workouts, and Programs.
    """
    trainer = TrainerSerializer(read_only=True)  # Read-only trainer details
    body_metrics = BodySerializer(read_only=True)  # Read-only body metrics
    exercises = ExerciseSerializer(many=True, read_only=True)  # List of related exercises
    workouts = WorkoutSerializer(many=True, read_only=True)  # List of related workouts
    programs = ProgramSerializer(many=True, read_only=True)  # List of related programs
    created_at = serializers.DateTimeField(read_only=True)  # Read-only creation timestamp
    full_name = serializers.CharField(read_only=True)  # Read-only computed full name

    class Meta:
        model = Client
        fields = '__all__'
        extra_kwargs = {
            'password': {'write_only': True},  # Hide password in responses
        }

    def create(self, validated_data):
        """
        Create a new Client instance with nested relationships.
        Expects IDs for trainer, body_metrics, exercises, workouts, and programs.
        """
        User = get_user_model()
        exercises_data = validated_data.pop('exercises', [])
        workouts_data = validated_data.pop('workouts', [])
        programs_data = validated_data.pop('programs', [])
        trainer_id = validated_data.pop('trainer', None)
        body_metrics_id = validated_data.pop('body_metrics', None)

        # Set password if provided
        password = validated_data.pop('password', None)
        client = User.objects.create_user(**validated_data)
        if password:
            client.set_password(password)

        # Set relationships
        if trainer_id:
            client.trainer_id = trainer_id
        if body_metrics_id:
            client.body_metrics_id = body_metrics_id
        client.save()

        if exercises_data:
            client.exercises.set(exercises_data)
        if workouts_data:
            client.workouts.set(workouts_data)
        if programs_data:
            client.programs.set(programs_data)

        return client

    def update(self, instance, validated_data):
        """
        Update existing Client instance and its relationships.
        Updates client fields and sets new relationship IDs.
        """
        User = get_user_model()
        exercises_data = validated_data.pop('exercises', [])
        workouts_data = validated_data.pop('workouts', [])
        programs_data = validated_data.pop('programs', [])
        trainer_id = validated_data.pop('trainer', None)
        body_metrics_id = validated_data.pop('body_metrics', None)

        # Update password if provided
        password = validated_data.pop('password', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:
            instance.set_password(password)
        instance.save()

        # Update relationships
        if trainer_id is not None:
            instance.trainer_id = trainer_id
        if body_metrics_id is not None:
            instance.body_metrics_id = body_metrics_id
        instance.save()

        if exercises_data:
            instance.exercises.set(exercises_data)
        if workouts_data:
            instance.workouts.set(workouts_data)
        if programs_data:
            instance.programs.set(programs_data)

        return instance
