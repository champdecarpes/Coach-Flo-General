from django.utils import timezone

from django.db import models
from django.core.exceptions import ValidationError


class Exercise(models.Model):
    name = models.CharField(max_length=75, default='')
    created_at = models.DateTimeField(default=timezone.now)

    # Trainer who created the program  # Ownership details
    ownership = models.ForeignKey('accounts.TrainerProfile', on_delete=models.CASCADE)
    visibility = models.CharField(max_length=20, choices=[
        ('public', 'Public'),
        ('private', 'Private')
    ], default='private')  # Visibility setting for the program

    # Exercise modality type
    modality = models.CharField(max_length=50, choices=[
        ('activation', 'Activation'),
        ('agility', 'Agility'),
        ('cardio', 'Cardio'),
        ('conditioning', 'Conditioning'),
        ('mobility', 'Mobility'),
        ('myofascial_release', 'Myofascial Release'),
        ('power', 'Power'),
        ('strength', 'Strength'),
        ('yoga', 'Yoga')
    ])
    # Targeted muscle group
    muscle_group = models.CharField(max_length=50, choices=[
        ('biceps', 'Biceps'),
        ('chest', 'Chest'),
        ('core', 'Core'),
        ('forearms', 'Forearms'),
        ('full_body', 'Full Body'),
        ('glutes', 'Glutes'),
        ('hamstrings', 'Hamstrings'),
        ('hip_and_groin', 'Hip & Groin'),
        ('lower_back', 'Lower Back'),
        ('lower_body', 'Lower Body'),
        ('lower_leg', 'Lower Leg'),
        ('mid_back', 'Mid Back'),
        ('quads', 'Quads'),
        ('shoulders', 'Shoulders'),
        ('triceps', 'Triceps'),
        ('upper_back_and_neck', 'Upper Back & Neck'),
        ('upper_body', 'Upper Body')
    ])
    # Movement pattern of the exercise
    movement_pattern = models.CharField(max_length=50, choices=[
        ('carry_gait', 'Carry / Gait'),
        ('core_bracing', 'Core Bracing'),
        ('core_flexion_extension', 'Core Flexion / Extension'),
        ('core_rotation', 'Core Rotation'),
        ('locomotion', 'Locomotion'),
        ('lower_body_hinge', 'Lower Body Hinge'),
        ('lower_body_push', 'Lower Body Push'),
        ('upper_body_horizontal_pull', 'Upper Body Horizontal Pull'),
        ('upper_body_horizontal_push', 'Upper Body Horizontal Push'),
        ('upper_body_vertical_pull', 'Upper Body Vertical Pull'),
        ('upper_body_vertical_push', 'Upper Body Vertical Push')
    ])

    # Instructions for performing the exercise
    instructions = models.TextField(max_length=500)
    # Links to additional resources
    links = models.TextField(max_length=500, blank=True)

    # note for the exercise
    note = models.CharField(max_length=100, blank=True)

    # Flag for each side execution
    each_side = models.BooleanField(default=False)


    # List of monitored field names (<=3)
    monitored_fields = models.JSONField(default=list, blank=True)

    def __self__(self):
        return self.id

    def clean(self):
        # Check that the number of monitored fields does not exceed 3
        if self.monitored_fields and len(self.monitored_fields) > 3:
            raise ValidationError("No more than 3 tracking fields")

    class Meta:
        verbose_name = "Exercise"
        verbose_name_plural = "Exercises"


class TrackingFields(models.Model):

    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    strength = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    bodyweight = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    timed = models.TimeField(default='00:00:00')
    distance_x_time = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)

    time = models.TimeField(default='00:00:00')
    speed = models.DecimalField(max_digits=10, decimal_places=2)

    # Cadence in steps per minute
    cadence = models.DecimalField(max_digits=5, decimal_places=3)
    # Distance in meters
    distance = models.DecimalField(max_digits=10, decimal_places=2)

    reps = models.IntegerField(default=0)
    # Weight in kilograms
    weight = models.DecimalField(max_digits=10, decimal_places=2)
    # Heart rate in beats per minute
    heart_rate = models.DecimalField(max_digits=10, decimal_places=2)
    # Percentage of maximum heart rate
    percentage_hr = models.DecimalField(max_digits=4, decimal_places=3)
    # Revolutions per minute
    rpm = models.DecimalField(max_digits=10, decimal_places=2)
    # Round field for custom tracking
    round_field = models.IntegerField()
    # Rest time
    rest = models.TimeField(default='00:00:00')

    def __str__(self):
        return f'{self.id}'

    class Meta:
        verbose_name = "Tracking Field"
        verbose_name_plural = "Tracking Fields"
