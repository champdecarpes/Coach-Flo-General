from django.db import models

class Exercise(models.Model):
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
    primary_focus = models.CharField(max_length=50)
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
    time = models.DecimalField(max_digits=10, decimal_places=2)
    speed = models.DecimalField(max_digits=10, decimal_places=2)
    cadence = models.DecimalField(max_digits=5, decimal_places=3)
    distance = models.DecimalField(max_digits=10, decimal_places=2)
    reps = models.IntegerField(max_digits=10, decimal_places=2)
    weight = models.DecimalField(max_digits=10, decimal_places=2)
    heart_rate = models.DecimalField(max_digits=10, decimal_places=2)
    percentage_hr = models.DecimalField(max_digits=4, decimal_places=3)
    rpm = models.DecimalField(max_digits=10, decimal_places=2)
    round_field = models.IntegerField(max_digits=10, decimal_places=2)
    rest = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        verbose_name = "Tracking Field"
        verbose_name_plural = "Tracking Fields"
