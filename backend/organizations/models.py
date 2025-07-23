from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import OneToOneField

from branding.models import Brand


class Organization(AbstractUser):
    name = models.CharField(max_length=100)

    # Clients have Organization ForeignKey to make OneToMany connection
    # Trainers have Organization ForeignKey to make OneToMany connection

    phone_number = models.CharField(max_length=20, blank=True, null=True)  # Client's phone number
    mail = models.EmailField(unique=True)  # Email for authentication (overrides email from AbstractUser)
    branding = OneToOneField(Brand, on_delete=models.CASCADE)

    USERNAME_FIELD = 'mail'  # Use email as username for login
    REQUIRED_FIELDS = ['mail']  # Required fields for user creation

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Organization'
        verbose_name = 'Organization'
