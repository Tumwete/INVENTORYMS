from django.contrib.auth.models import User
from .models import Profile
from django.db.models.signals import post_save
from django.dispatch import receiver


# creating the user profile
@receiver(post_save,sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(staff=instance)

# saving the profile (so created is not passed as a parameter)
@receiver(post_save,sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()