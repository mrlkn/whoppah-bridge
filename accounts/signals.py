from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import User, CourierProfile, CustomerProfile


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Create the appropriate profile when a user is created."""
    if created:
        if instance.user_type == User.Types.COURIER and not hasattr(instance, 'courier_profile'):
            CourierProfile.objects.create(user=instance)
        elif instance.user_type == User.Types.CUSTOMER and not hasattr(instance, 'customer_profile'):
            CustomerProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """Save the user profile whenever the user is saved."""
    if instance.user_type == User.Types.COURIER and hasattr(instance, 'courier_profile'):
        instance.courier_profile.save()
    elif instance.user_type == User.Types.CUSTOMER and hasattr(instance, 'customer_profile'):
        instance.customer_profile.save()
