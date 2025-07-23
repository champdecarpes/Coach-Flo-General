from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from organizations.models import Organization


class Trainer(AbstractUser):
    """
    Model representing a trainer with authentication and client-related data.
    Inherits from AbstractUser for authentication functionality.
    """
    created_at = models.DateTimeField(default=timezone.now, editable=False)  # Creation timestamp

    sex = models.CharField(max_length=6, choices=[
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other')
    ], default='O')

    first_name = models.CharField(max_length=50)  # First name part of full name
    second_name = models.CharField(max_length=50, blank=True, null=True)  # Second name part of full name
    full_name = models.CharField(max_length=101, editable=False)  # Computed full name

    birthdate = models.DateField(null=True, blank=True)  # Date of birth
    phone_number = models.CharField(max_length=20, blank=True, null=True)  # Client's phone number
    mail = models.EmailField(unique=True)  # Email for authentication (overrides email from AbstractUser)

    organization = models.ForeignKey(Organization, on_delete=models.SET_NULL, null=True)

    USERNAME_FIELD = 'mail'  # Use email as username for login
    REQUIRED_FIELDS = ['first_name', 'second_name']  # Required fields for user creation

    def save(self, *args, **kwargs):
        """
        Override save method to compute full_name and prevent its manual modification.
        """
        if not self.full_name or self.full_name != f"{self.first_name} {self.second_name or ''}".strip():
            self.full_name = f"{self.first_name} {self.second_name or ''}".strip()
        super().save(*args, **kwargs)

    def __str__(self):
        """
        String representation of the trainer.
        """
        return self.full_name or self.mail

    class Meta:
        verbose_name = "Trainer"
        verbose_name_plural = "Trainers"
        permissions = [
            ("view_own_data", "Can view own trainer data and clients connected to the trainer"),
        ]


class SelfTask(models.Model):
    """
    Model representing a self-assigned task for a trainer.
    """
    name = models.CharField(max_length=50, unique=True)  # Task name
    description = models.TextField()  # Task description
    date = models.DateField(default=timezone.now)  # Task date

    trainer = models.ForeignKey(Trainer, on_delete=models.CASCADE)

    def __str__(self):
        """
        String representation of the task.
        """
        return self.name

    class Meta:
        verbose_name = "Self Task"
        verbose_name_plural = "Self Tasks"
