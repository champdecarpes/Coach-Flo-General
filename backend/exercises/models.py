from django.db import models

class Exercise(models.Model):
    modality = models.CharField(max_length=50)
    primary_focus = models.CharField(max_length=50)
    muscle_group = models.CharField(max_length=50)
    movement_pattern = models.CharField(max_length=50)
    strength = models.CharField(max_length=50)
    bodyweight = models.CharField(max_length=50)
    timed = models.CharField(max_length=50)
    distance_x_time = models.CharField(max_length=50)
    category = models.CharField(max_length=50)
    instructions = models.TextField()
    links = models.TextField()
    advanced_settings = models.TextField()
    tracking_fields = models.ManyToManyField('TrackingFields', limit_choices_to={'id__lte': 3})

    class Meta:
        verbose_name = "Exercise"
        verbose_name_plural = "Exercises"

class TrackingFields(models.Model):
    time = models.CharField(max_length=50)
    speed = models.CharField(max_length=50)
    cadence = models.CharField(max_length=50)
    distance = models.CharField(max_length=50)
    reps = models.CharField(max_length=50)
    weight = models.CharField(max_length=50)
    heart_rate = models.CharField(max_length=50)
    percentage_hr = models.CharField(max_length=50)
    rpm = models.CharField(max_length=50)
    round_field = models.CharField(max_length=50)
    rest = models.CharField(max_length=50)

    class Meta:
        verbose_name = "Tracking Field"
        verbose_name_plural = "Tracking Fields"
