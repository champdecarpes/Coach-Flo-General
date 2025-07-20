from django.db import models


class Section(models.Model):
    name = models.CharField(max_length=75)
    created_at = models.DateTimeField(auto_now_add=True)

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
