from django.db import models
from django.utils import timezone
from accounts.models import TrainerProfile


class Program(models.Model):
    """
    Program model representing a multi-day program with Workouts and Sections
    Contains Workouts and Sections that can be customized per day
    """

    name = models.CharField(max_length=75)  # Program name
    created_at = models.DateTimeField(default=timezone.now)  # Creation timestamp
    workouts = models.ManyToManyField('workouts.Workout', blank=True)  # Related Workouts
    sections = models.ManyToManyField('sections.Section', blank=True)  # Related Sections
    exercises = models.ManyToManyField('exercises.Exercise', blank=True)  # Related Exercises

    start_date = models.DateField(default=timezone.now)
    end_date = models.DateField(default=timezone.now)

    # Trainer who created the program
    ownership = models.ForeignKey('accounts.TrainerProfile', on_delete=models.CASCADE, null=True)
    visibility = models.CharField(max_length=20, choices=[
        ('public', 'Public'),
        ('private', 'Private')
    ], default='private')  # Visibility setting for the program

    description = models.TextField(blank=True, null=True)  # Program description

    class Meta:
        verbose_name = "Program"
        verbose_name_plural = "Programs"
