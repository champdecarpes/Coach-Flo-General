from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class BaseUserModel(AbstractUser):
    created_at = models.DateTimeField(default=timezone.now, editable=False)  # Creation timestamp

    name = models.CharField(max_length=50)  # Computed full name
    username = models.CharField(max_length=50, unique=True)
    self_description = models.TextField(blank=True, null=True)

    phone_number = models.CharField(max_length=20, blank=True, null=True)  # Client's phone number
    mail = models.EmailField(unique=True)  # Email for authentication (overrides email from AbstractUser)


    # Gender
    sex = models.CharField(max_length=6, choices=[
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other')
    ], default='O')

    USERNAME_FIELD = ['mail']  # Use email as username for login
    REQUIRED_FIELDS = ['username', 'name']  # Required fields for user creation


    def __str__(self):
        return {'username': self.username, 'email': self.email}
