from django.db import models
class Trainer(models.Model):
    name = models.CharField(max_length=100)
    sex = models.CharField(max_length=6, choices=[
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other')
    ])
    age = models.IntegerField(max_length=6)
