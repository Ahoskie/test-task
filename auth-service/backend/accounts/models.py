from django.contrib.auth.models import User
from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.db.models.signals import post_save
from django.dispatch.dispatcher import receiver


class UserProfile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile',
    )
    last_request_time = models.DateTimeField(null=True, blank=True)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance, last_request_time=instance.last_login)
    else:
        instance.profile.save()
