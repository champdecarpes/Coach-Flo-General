from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Trainer, SelfTask
from organizations.serializers import OrganizationSerializer  # Assuming OrganizationSerializer exists


class SelfTaskSerializer(serializers.ModelSerializer):
    """
    Serializer for the SelfTask model.
    Handles the relationship with the Trainer.
    """
    trainer = serializers.PrimaryKeyRelatedField(queryset=Trainer.objects.all(), required=False)  # Trainer ID

    class Meta:
        model = SelfTask
        fields = '__all__'

    def create(self, validated_data):
        """
        Create a new SelfTask instance with its Trainer relationship.
        """
        trainer_id = validated_data.pop('trainer', None)
        self_task = SelfTask.objects.create(**validated_data)
        if trainer_id:
            self_task.trainer_id = trainer_id
            self_task.save()
        return self_task

    def update(self, instance, validated_data):
        """
        Update existing SelfTask instance and its Trainer relationship.
        """
        trainer_id = validated_data.pop('trainer', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if trainer_id is not None:
            instance.trainer_id = trainer_id
        instance.save()
        return instance


class TrainerSerializer(serializers.ModelSerializer):
    """
    Serializer for the Trainer model.
    Handles nested relationships with Organization and self-assigned tasks.
    """
    organization = OrganizationSerializer(read_only=True)  # Read-only organization details
    created_at = serializers.DateTimeField(read_only=True)  # Read-only creation timestamp
    full_name = serializers.CharField(read_only=True)  # Read-only computed full name
    self_tasks = SelfTaskSerializer(many=True, read_only=True)  # List of related self-tasks

    class Meta:
        model = Trainer
        fields = '__all__'
        extra_kwargs = {
            'password': {'write_only': True},  # Hide password in responses
        }

    def create(self, validated_data):
        """
        Create a new Trainer instance with nested relationships.
        Expects IDs for organization and self-tasks.
        """
        User = get_user_model()
        self_tasks_data = validated_data.pop('self_tasks', [])
        organization_id = validated_data.pop('organization', None)

        # Set password if provided
        password = validated_data.pop('password', None)
        trainer = User.objects.create_user(**validated_data)
        if password:
            trainer.set_password(password)

        # Set relationships
        if organization_id:
            trainer.organization_id = organization_id
            trainer.save()

        # Handle self-tasks (create separately if needed)
        if self_tasks_data:
            for task_data in self_tasks_data:
                SelfTask.objects.create(trainer=trainer, **task_data)

        return trainer

    def update(self, instance, validated_data):
        """
        Update existing Trainer instance and its relationships.
        Updates trainer fields and sets new relationship IDs.
        """
        User = get_user_model()
        self_tasks_data = validated_data.pop('self_tasks', [])
        organization_id = validated_data.pop('organization', None)

        # Update password if provided
        password = validated_data.pop('password', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:
            instance.set_password(password)
        instance.save()

        # Update relationships
        if organization_id is not None:
            instance.organization_id = organization_id
            instance.save()

        # Handle self-tasks (delete and recreate for simplicity)
        if self_tasks_data:
            instance.self_tasks.all().delete()
            for task_data in self_tasks_data:
                SelfTask.objects.create(trainer=instance, **task_data)

        return instance
