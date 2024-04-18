from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from users.models import Wallet


@receiver(post_save, sender=User)
def settlement(sender, instance, created, **kwargs):
    if created:
        Wallet.objects.create(user=instance)