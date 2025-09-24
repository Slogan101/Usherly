from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import UsherProfile, HostProfile, CustomUser



@receiver(post_save, sender=CustomUser)
def create_profile(sender, instance, created, **kwargs):
    if created:
        if instance.user_type == 'usher':
            # get_or_create is used to avoid duplicate creation in edge cases.
            UsherProfile.objects.get_or_create(user=instance)
        elif instance.user_type == 'host':
            HostProfile.objects.get_or_create(user=instance)

@receiver(post_save, sender=CustomUser)
def save(sender, instance, **kwargs):
    instance.profile.save()