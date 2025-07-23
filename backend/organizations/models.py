from django.db import models
from django.db.models import OneToOneField

from base_models.models import BaseUserModel
from branding.models import Brand


class Organization(BaseUserModel):

    # Clients have Organization ForeignKey to make OneToMany connection
    # Trainers have Organization ForeignKey to make OneToMany connection

    branding = OneToOneField(Brand, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True, editable=False)

    class Meta:
        verbose_name_plural = 'Organization'
        verbose_name = 'Organization'
