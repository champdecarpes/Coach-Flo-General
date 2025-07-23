from django.db import models
from django.utils import timezone

from base_models.models import BaseUserModel
from programs.models import Program
from trainers.models import Trainer
from exercises.models import Exercise
from bodies.models import Body  # Assuming BodyMetrics model exists
from workouts.models import Workout


class Client(BaseUserModel):
    """
    Model representing a client with authentication and fitness-related data
    Inherits from AbstractUser for authentication functionality
    """
    birthdate = models.DateField(null=True, blank=True)  # Date of birth

    trainer = models.ForeignKey(Trainer, on_delete=models.SET_NULL)  # Assigned trainer
    body_metrics = models.OneToOneField(Body, on_delete=models.CASCADE)  # Client's metrics

    # Training specific
    exercises = models.ManyToManyField(Exercise, blank=True, null=True)  # Exercises assigned to client
    workouts = models.ManyToManyField(Workout, blank=True, null=True)  # Workout assigned to client
    programs = models.ManyToManyField(Program, blank=True, null=True)  # Multi days Program assigned to client


    class Meta:
        verbose_name = "Client"
        verbose_name_plural = "Clients"
        permissions = [
            ("view_own_data", "Can view own client data"),  # Custom permission for limited access
        ]
