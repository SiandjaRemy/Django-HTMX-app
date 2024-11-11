from django.dispatch import receiver
from django.db.models.signals import post_save

from django.contrib.auth import get_user_model

from a_users.models import Profile

User = get_user_model()


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
        
    else:
        profile = Profile.objects.filter(user=instance).first()
        profile.email = instance.email
        profile.save()
        

@receiver(post_save, sender=Profile)
def create_user_profile(sender, instance, created, **kwargs):
    if not created:
        user = User.objects.only("email").filter(id=instance.user.id).first()
        if user.email != instance.email:
            user.email = instance.email
            user.save()

