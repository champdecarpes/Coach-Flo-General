from django.db import models
from django.utils import timezone



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

    exercises = models.ManyToManyField('exercises.Exercise', blank=True)  # Related Exercises

    start_time = models.TimeField(default='00:00:00', blank=True, null=True)  # Section duration

    rounds = models.IntegerField(default=0, blank=True, null=True)  # Number of rounds
    duration = models.TimeField(blank=True, null=True)  # Duration time
    rest = models.TimeField(blank=True, null=True)  # Rest duration

    note = models.TextField(blank=True, default='')  # Additional notes

    class Meta:
        verbose_name = "Section"
        verbose_name_plural = "Sections"
