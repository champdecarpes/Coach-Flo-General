from rest_framework import serializers
from accounts.models import User, OrganizationProfile, TrainerProfile, SelfTask, \
    ClientProfile  # Assuming these are defined elsewhere
from bodies.models import Body
from branding.models import Brand
from exercises.models import Exercise
from programs.models import Program
from workouts.models import Workout


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for User model
    Handles basic user data including role and authentication fields
    """

    class Meta:
        model = User
        fields = '__all__'


class BrandSerializer(serializers.ModelSerializer):
    """
    Serializer for Brand model
    Handles branding data for organizations
    """

    class Meta:
        model = Brand
        fields = '__all__'


class OrganizationProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for OrganizationProfile model
    Includes nested user and branding data
    """
    user = UserSerializer()
    branding = BrandSerializer()

    class Meta:
        model = OrganizationProfile
        fields = '__all__'


class TrainerProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for TrainerProfile model
    Includes nested user and organization data
    """
    user = UserSerializer()
    organization = OrganizationProfileSerializer()

    class Meta:
        model = TrainerProfile
        fields = '__all__'


class SelfTaskSerializer(serializers.ModelSerializer):
    """
    Serializer for SelfTask model
    Includes nested trainer data
    """
    trainer = TrainerProfileSerializer()

    class Meta:
        model = SelfTask
        fields = '__all__'


class BodySerializer(serializers.ModelSerializer):
    """
    Serializer for Body model
    Handles client body metrics data
    """

    class Meta:
        model = Body
        fields = '__all__'


class ClientProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for ClientProfile model
    Includes nested user, trainer, body metrics, organization, exercises, workouts, and programs
    """
    user = UserSerializer()
    trainer = TrainerProfileSerializer()
    body_metrics = BodySerializer()
    organization = OrganizationProfileSerializer()
    exercises = serializers.PrimaryKeyRelatedField(many=True, queryset=Exercise.objects.all(), required=False)
    workouts = serializers.PrimaryKeyRelatedField(many=True, queryset=Workout.objects.all(), required=False)
    programs = serializers.PrimaryKeyRelatedField(many=True, queryset=Program.objects.all(), required=False)

    class Meta:
        model = ClientProfile
        fields = '__all__'
