from django.db import models
from django.utils import timezone

from exercises.models import Exercise
from trainers.models import Trainer
from sections.models import Section


class Workout(models.Model):
    """
    Workout model representing a daily exercise plan with Sections and Exercises
    Can include Sections and Exercises directly
    """
    name = models.CharField(max_length=75, default='')  # Workout name
    created_at = models.DateTimeField(default=timezone.now)  # Creation timestamp
    description = models.TextField(blank=True, null=True)  # Workout description

    sections = models.ManyToManyField("Section", blank=True)  # Related Sections
    exercises = models.ManyToManyField(Exercise, blank=True)  # Related Exercises

    # Trainer who created the program  # Ownership details
    ownership = models.ForeignKey(Trainer, on_delete=models.CASCADE)
    visibility = models.CharField(max_length=20, choices=[
        ('public', 'Public'),
        ('private', 'Private')
    ], default='private')  # Visibility setting for the program

    class Meta:
        verbose_name = "Workout"
        verbose_name_plural = "Workouts"
