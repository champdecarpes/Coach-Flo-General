from django.db.models.signals import post_save
from django.dispatch import receiver

from accounts.models import TrainerProfile, ClientProfile, OrganizationProfile, User


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        if instance.role == 'trainer':
            TrainerProfile.objects.create(user=instance)
        elif instance.role == 'client':
            ClientProfile.objects.create(user=instance)
        elif instance.role == 'organization':
            OrganizationProfile.objects.create(user=instance)
