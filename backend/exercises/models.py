from django.db import models
from django.core.exceptions import ValidationError


class Exercise(models.Model):
    modality = models.TextField(choices=[
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
    muscle_group = models.TextField(choices=[
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
    movement_pattern = models.TextField(choices=[
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
    strength = models.DecimalField(max_length=5, decimal_places=2, default=0)
    bodyweight = models.DecimalField(max_length=5, decimal_places=2, default=0)
    timed = models.TimeField(default=0)
    distance_x_time = models.DecimalField(max_length=50, default=0.0, decimal_places=2)
    instructions = models.TextField(max_length=500, default='')
    links = models.TextField(max_length=500, default='')
    default_note = models.TextField(max_length=500, default='')

    # Все возможные поля для мониторинга
    tracking_fields = models.OneToOneField('TrackingFields',on_delete=models.CASCADE)

    # Только названия полей, которые мониторятся
    monitored_fields = models.JSONField(default=list, blank=True)

    def clean(self):
        # Проверка, что количество названий полей не превышает 3
        if self.monitored_fields and len(self.monitored_fields) > 3:
            raise ValidationError("Можно мониторить не более 3 полей.")

    class Meta:
        verbose_name = "Exercise"
        verbose_name_plural = "Exercises"

class TrackingFields(models.Model):
    time = models.TimeField(max_digits=10, decimal_places=2)
    speed = models.DecimalField(max_digits=10, decimal_places=2)
    cadence = models.DecimalField(max_digits=5, decimal_places=3)
    distance = models.DecimalField(max_digits=10, decimal_places=2)
    reps = models.IntegerField(default=0)
    weight = models.DecimalField(max_digits=10, decimal_places=2)
    heart_rate = models.DecimalField(max_digits=10, decimal_places=2)
    percentage_hr = models.DecimalField(max_digits=4, decimal_places=3)
    rpm = models.DecimalField(max_digits=10, decimal_places=2)
    round_field = models.IntegerField()
    rest = models.TimeField(max_digits=10, decimal_places=2)

    class Meta:
        verbose_name = "Tracking Field"
        verbose_name_plural = "Tracking Fields"
