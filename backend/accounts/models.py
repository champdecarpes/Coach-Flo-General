from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import OneToOneField
from django.utils import timezone



class User(AbstractUser):
    role = models.CharField(max_length=20, choices=[
        ('trainer', 'Trainer'),
        ('client', 'Client'),
        ('organization', 'Organization')
    ], default='client')

    self_description = models.TextField(blank=True, null=True)

    # Email for authentication (overrides email from AbstractUser)
    email = models.EmailField(max_length=254, unique=True, blank=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)  # Client's phone number
    birthday = models.DateField(null=True, blank=True)  # Date of birth

    # Gender
    gender = models.CharField(max_length=6, choices=[
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other')
    ], default='O')

    USERNAME_FIELD = 'email'  # Use email as username for login
    REQUIRED_FIELDS = ['username', 'birthday']  # Required fields for user creation

    def __str__(self):
        return f'{self.username}, {self.email}'

    class Meta:
        verbose_name = 'Basic User Model'


class OrganizationProfile(models.Model):

    # Clients have Organization ForeignKey to make OneToMany connection
    # Trainers have Organization ForeignKey to make OneToMany connection

    user = models.OneToOneField('User', on_delete=models.CASCADE)
    branding = OneToOneField('branding.Brand', on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = 'Organization'
        verbose_name = 'Organization'


class TrainerProfile(models.Model):
    """
    Model representing a trainer with authentication and client-related data.
    """

    user = models.OneToOneField('User', on_delete=models.CASCADE)
    organization = models.ForeignKey('OrganizationProfile', on_delete=models.SET_NULL, null=True)

    class Meta:
        verbose_name = "Trainer"
        verbose_name_plural = "Trainers"
        # permissions = [
        #     ("view_own_data", "Can view own trainer data and clients connected to the trainer"),
        # ]


class SelfTask(models.Model):
    """
    Model representing a self-assigned task for a trainer
    """
    created_at = models.DateTimeField(default=timezone.now, editable=False)  # Creation timestamp

    name = models.CharField(max_length=50)  # Task name
    description = models.TextField()  # Task description
    date = models.DateField(default=timezone.now)  # Task date
    done = models.BooleanField(default=False)

    trainer = models.ForeignKey('TrainerProfile', on_delete=models.CASCADE)

    def __str__(self):
        """
        String representation of the task
        """
        return self.name

    class Meta:
        verbose_name = "Self Task"
        verbose_name_plural = "Self Tasks"


class ClientProfile(models.Model):
    """
    Model representing a client with authentication and fitness-related data
    """

    user = models.OneToOneField('User', on_delete=models.CASCADE)
    trainer = models.ForeignKey('TrainerProfile', on_delete=models.SET_NULL, null=True)  # Assigned trainer
    body_metrics = models.OneToOneField('bodies.Body', on_delete=models.CASCADE)  # Client's metrics
    organization = models.ForeignKey('OrganizationProfile', on_delete=models.SET_NULL, null=True)

    # Training specific
    exercises = models.ManyToManyField('exercises.Exercise', blank=True, null=True)  # Exercises assigned to client
    workouts = models.ManyToManyField('workouts.Workout', blank=True, null=True)  # Workout assigned to client
    programs = models.ManyToManyField('programs.Program', blank=True, null=True)  # Multi days Program assigned to client

    class Meta:
        verbose_name = "Client"
        verbose_name_plural = "Clients"
        # permissions = [
        #     ("view_own_data", "Can view own client data"),  # Custom permission for limited access
        # ]
