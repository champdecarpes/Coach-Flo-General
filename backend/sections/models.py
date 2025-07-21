from django.db import models
from django.utils import timezone

from exercises.models import Exercise
from trainers.models import Trainer


class Program(models.Model):
    """
    Program model representing a multi-day program with Workouts and Sections
    Contains Workouts and Sections that can be customized per day
    """
    name = models.CharField(max_length=75)  # Program name
    created_at = models.DateTimeField(default=timezone.now)  # Creation timestamp
    workouts = models.ManyToManyField("Workout", blank=True)  # Related Workouts
    sections = models.ManyToManyField("Section", blank=True)  # Related Sections
    exercises = models.ManyToManyField("Exercise", blank=True)  # Related Exercises

    start_date = models.DateField(default=timezone.now)
    end_date = models.DateField(default=timezone.now)

    ownership = models.ForeignKey(Trainer, on_delete=models.CASCADE, null=True,
                                  blank=True)  # Trainer who created the program  # Ownership details
    visibility = models.CharField(max_length=20, choices=[
        ('public', 'Public'),
        ('private', 'Private')
    ], default='private')  # Visibility setting for the program

    description = models.TextField(blank=True, null=True)  # Program description

    class Meta:
        verbose_name = "Program"
        verbose_name_plural = "Programs"


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


class Section(models.Model):
    """
    Model representing a section with multiple Exercises
    Part of a Workout with specific type and settings
    """
    name = models.CharField(max_length=75, default='')  # Section name
    created_at = models.DateTimeField(default=timezone.now)  # Creation timestamp

    section_type = models.CharField(max_length=50, choices=[
        ('regular', 'Regular'),
        ('interval', 'Interval'),
        ('amrap', 'AsMuchRepeatAsPossible'),
        ('timed', 'Timed'),
        ('freestyle', 'Freestyle')
    ])  # Type of section

    exercises = models.ManyToManyField(Exercise, blank=True)  # Related Exercises

    start_time = models.TimeField(default='00:00:00', blank=True, null=True)  # Section duration

    rounds = models.IntegerField(default=0, blank=True, null=True)  # Number of rounds
    duration = models.TimeField(blank=True, null=True)  # Duration time
    rest = models.TimeField(blank=True, null=True)  # Rest duration

    note = models.TextField(blank=True, default='')  # Additional notes

    class Meta:
        verbose_name = "Section"
        verbose_name_plural = "Sections"
