from rest_framework import serializers
from .models import Task
from bodies.models import Body
from bodies.serializers import BodySerializer 


class TaskSerializer(serializers.ModelSerializer):
    """
    Serializer for Task model
    Includes all fields from Task and nested BodySerializer for body_metric
    """
    body_metric = BodySerializer()  # Nested serializer for body_metric field

    class Meta:
        model = Task
        fields = ['id', 'name', 'date', 'note', 'done', 'body_metric']
        read_only_fields = ['id', 'date']  # id and date are auto-generated

    def validate_name(self, value):
        """
        Validate that the name field is not empty
        """
        if not value.strip():
            raise serializers.ValidationError("Name cannot be empty")
        return value

    def create(self, validated_data):
        """
        Create method to handle creation of Task with nested Body data
        Validates and creates Body instance before creating Task
        """
        body_data = validated_data.pop('body_metric')  # Extract nested body data
        body_serializer = BodySerializer(data=body_data)
        if body_serializer.is_valid(raise_exception=True):
            body_instance = body_serializer.save()  # Create Body instance
            task = Task.objects.create(body_metric=body_instance, **validated_data)  # Create Task
            return task
        return None  # This line is unreachable due to raise_exception=True

    def update(self, instance, validated_data):
        """
        Update method to handle updating Task and nested Body data
        Updates Body instance if body_metric data is provided
        """
        body_data = validated_data.pop('body_metric', None)  # Extract body data if provided
        task = super().update(instance, validated_data)  # Update Task fields

        if body_data:
            body_serializer = BodySerializer(task.body_metric, data=body_data)
            if body_serializer.is_valid(raise_exception=True):
                body_serializer.save()  # Update Body instance
        return task
