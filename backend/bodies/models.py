from django.db import models
from django.utils import timezone


class Body(models.Model):
    """
    Model for storing athlete's body metrics
    """
    body_fat = models.DecimalField(max_digits=5, decimal_places=2, default=0)  # Percentage of body fat
    weight = models.DecimalField(max_digits=5, decimal_places=2, default=0)  # Weight in kilograms
    body_fat_mass = models.DecimalField(max_digits=5, decimal_places=2, default=0)  # Mass of body fat
    lean_body_mass = models.DecimalField(max_digits=5, decimal_places=2, default=0)  # Lean body mass
    chest = models.DecimalField(max_digits=5, decimal_places=2, default=0)  # Chest circumference
    shoulder = models.DecimalField(max_digits=5, decimal_places=2, default=0)  # Shoulder circumference
    waist = models.DecimalField(max_digits=5, decimal_places=2, default=0)  # Waist circumference
    resting_heart_rate = models.IntegerField(default=0)  # Resting heart rate in beats per minute
    thigh_left = models.DecimalField(max_digits=5, decimal_places=2, default=0)  # Left thigh circumference
    thigh_right = models.DecimalField(max_digits=5, decimal_places=2, default=0)  # Right thigh circumference
    hip = models.DecimalField(max_digits=5, decimal_places=2, default=0)  # Hip circumference
    calf_left = models.DecimalField(max_digits=5, decimal_places=2, default=0)  # Left calf circumference
    calf_right = models.DecimalField(max_digits=5, decimal_places=2, default=0)  # Right calf circumference
    height = models.DecimalField(max_digits=5, decimal_places=2, default=0)  # Height in meters
    bicep_left = models.DecimalField(max_digits=5, decimal_places=2, default=0)  # Left bicep circumference
    bicep_right = models.DecimalField(max_digits=5, decimal_places=2, default=0)  # Right bicep circumference
    steps = models.IntegerField(default=0)  # Daily step count
    sleep = models.IntegerField(default=0)  # Sleep duration in hours

    def __str__(self):
        return f"Body metrics {self.id}"

    def save(self, *args, **kwargs):
        """
        Overrides save method to track all changes over time
        Compares current instance with database state and logs changes
        """
        if self.pk:  # Check if instance already exists in database
            try:
                old_instance = Body.objects.get(pk=self.pk)
                for field in self._meta.fields:
                    if field.name not in ['id']:  # Exclude non-trackable fields
                        current_value = getattr(self, field.name)
                        old_value = getattr(old_instance, field.name)
                        if str(current_value) != str(old_value):  # Compare values as strings
                            BodyChangeHistory.objects.create(
                                body=self,
                                field_name=field.name,
                                old_value=str(old_value),
                                new_value=str(current_value)
                            )
            except Body.DoesNotExist:
                pass
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Body"
        verbose_name_plural = "Body metrics"


class BodyChangeHistory(models.Model):
    """
    Model for storing history of changes to Body metrics
    """
    body = models.ForeignKey(Body, on_delete=models.CASCADE)  # Reference to the Body instance
    field_name = models.CharField(max_length=50)  # Name of the modified field
    old_value = models.CharField(max_length=100, blank=True, null=True)  # Old value of the field
    new_value = models.CharField(max_length=100)  # New value of the field
    timestamp = models.DateTimeField(default=timezone.now)  # Time of the change

    def __str__(self):
        return f"Change to {self.field_name} at {self.timestamp}"

    class Meta:
        verbose_name = "Body Change History"
        verbose_name_plural = "Body Change Histories"
