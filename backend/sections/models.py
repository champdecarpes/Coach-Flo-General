from django.db import models

class Section(models.Model):
    name = models.CharField(max_length=100)
    section_type = models.CharField(max_length=50, choices=[
        ('regular', 'Regular'),
        ('interval', 'Interval'),
        ('amrap', 'AMRAP'),
        ('timed', 'Timed'),
        ('freestyle', 'Freestyle')
    ])
    duration = models.DecimalField(max_length=)
    rounds = models.IntegerField(max_length=3)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Section"
        verbose_name_plural = "Sections"
