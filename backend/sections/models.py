from django.db import models

# Сделать CustomField в зависимости от поля, которое выбирается в section_type

class Section(models.Model):
    name = models.CharField(max_length=100)
    section_type = models.CharField(max_length=50, choices=[
        ('regular', 'Regular'),
        ('interval', 'Interval'),
        ('amrap', 'AMRAP'),
        ('timed', 'Timed'),
        ('freestyle', 'Freestyle')
    ])
    regular_def_fields = models.TextField()
    interval_def_fields = models.TextField()
    amrap_def_fields = models.TextField()
    duration = models.CharField(max_length=50)
    timed_def_fields = models.TextField()
    rounds = models.CharField(max_length=50)
    freestyle_name = models.CharField(max_length=100)

    class Meta:
        verbose_name = "Section"
        verbose_name_plural = "Sections"
