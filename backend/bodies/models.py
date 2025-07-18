from django.db import models

class Body(models.Model):
    """
    Модель для хранения показателей тела спортсмена.
    """
    body_fat = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    weight = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    body_fat_mass = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    lean_body_mass = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    chest = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    shoulder = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    waist = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    resting_heart_rate = models.IntegerField(default=0)
    thigh_left = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    thigh_right = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    hip = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    calf_left = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    calf_right = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    height = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    bicep_left = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    bicep_right = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    steps = models.IntegerField(default=0)
    sleep = models.IntegerField(default=0)

    def __str__(self):
        return f"Показатели тела {self.id}"
