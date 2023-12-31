from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model

from .models import Profile

User = get_user_model()


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    '''Create an initial user profile.'''    
    
    if created: # check create the user profile or not
        Profile.objects.create(owner=instance)
