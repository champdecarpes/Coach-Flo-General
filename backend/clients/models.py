from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

from programs.models import Program
from trainers.models import Trainer
from exercises.models import Exercise
from bodies.models import Body  # Assuming BodyMetrics model exists
from workouts.models import Workout


class Client(AbstractUser):
    """
    Model representing a client with authentication and fitness-related data
    Inherits from AbstractUser for authentication functionality
    """
    sex = models.CharField(max_length=10, choices=[
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other')
    ], default='O')
    # Gender
    created_at = models.DateTimeField(default=timezone.now)  # Creation timestamp

    first_name = models.CharField(max_length=50)  # First name part of full name
    second_name = models.CharField(max_length=50, blank=True, null=True)  # Second name part of full name
    full_name = models.CharField(max_length=101, editable=False)  # Computed full name

    birthdate = models.DateField(null=True, blank=True)  # Date of birth
    phone_number = models.CharField(max_length=20, blank=True, null=True)  # Client's phone number
    mail = models.EmailField(unique=True)  # Email for authentication (overrides email from AbstractUser)

    trainer = models.ForeignKey(Trainer, on_delete=models.SET_NULL)  # Assigned trainer
    body_metrics = models.OneToOneField(Body, on_delete=models.CASCADE)  # Client's metrics

    # Training specific
    exercises = models.ManyToManyField(Exercise, blank=True, null=True)  # Exercises assigned to client
    workouts = models.ManyToManyField(Workout, blank=True, null=True)  # Workout assigned to client
    programs = models.ManyToManyField(Program, blank=True, null=True)  # Multi days Program assigned to client

    USERNAME_FIELD = 'mail'  # Use email as username for login
    REQUIRED_FIELDS = ['mail']  # Required fields for user creation

    def save(self, *args, **kwargs):
        """
        Override save method to compute full_name and prevent its manual modification.
        """
        self.full_name = f"{self.first_name} {self.second_name or ''}".strip()
        super().save(*args, **kwargs)

    def __str__(self):
        """
        String representation of the client.
        """
        return self.full_name or self.mail

    class Meta:
        verbose_name = "Client"
        verbose_name_plural = "Clients"
        permissions = [
            ("view_own_data", "Can view own client data"),  # Custom permission for limited access
        ]
