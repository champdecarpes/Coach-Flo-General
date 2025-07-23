from django.db import models
from django.utils import timezone

from base_models.models import BaseUserModel
from organizations.models import Organization


class Trainer(BaseUserModel):
    """
    Model representing a trainer with authentication and client-related data.
    Inherits from AbstractUser for authentication functionality.
    """

    birthdate = models.DateField(null=True, blank=True)  # Date of birth
    organization = models.ForeignKey(Organization, on_delete=models.SET_NULL, null=True)


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
