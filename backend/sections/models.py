from django.utils import timezone

from django.db import models


class Program(models.Model):
    """
    Program with Workouts for several days
    """
    name = models.CharField(max_length=75)
    created_at = models.DateTimeField(default=timezone.now)
    section = models.ManyToManyField("Section", on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Program"
        verbose_name_plural = "Programs"


class Workout(models.Model):
    """
    Workout for one day, with several Sections / Exercises
    """
    name = models.CharField(max_length=75, default='')
    created_at = models.DateTimeField(default=timezone.now)
    section = models.ManyToManyField("Section", on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Workout"
        verbose_name_plural = "Workouts"


class Section(models.Model):
    """
    Section with several Exercises
    """
    name = models.CharField(max_length=75, default='')
    created_at = models.DateTimeField(default=timezone.now)

    section_type = models.CharField(max_length=50, choices=[
        ('regular', 'Regular'),
        ('interval', 'Interval'),
        ('amrap', 'AMRAP'),
        ('timed', 'Timed'),
        ('freestyle', 'Freestyle')
    ])
    duration = models.DecimalField(max_digits=5, decimal_places=2, default=0, blank=True, null=True)
    rounds = models.IntegerField(default=0, blank=True, null=True)

    class Meta:
        verbose_name = "Section"
        verbose_name_plural = "Sections"
