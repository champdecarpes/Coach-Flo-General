from django.utils import timezone

from django.db import models
from django.db.models import OneToOneField

from bodies.models import Body

class Task(models.Model):
    name = models.CharField(max_length=100, default='')
    date = models.DateTimeField(default=timezone.now)
    note = models.TextField(blank=True, null=True)
    done = models.BooleanField(default=False)
    body_metric = OneToOneField(Body, on_delete=models.CASCADE)
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Task'
        verbose_name_plural = 'Tasks'
