from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import Order


@receiver(pre_save, sender=Order)
def set_partner_company_from_courier(sender, instance, **kwargs):
    """
    Signal handler to automatically set the partner company on an order
    when a courier is assigned.
    """
    # If the order has an assigned courier but no partner company
    if instance.assigned_courier and not instance.partner_company:
        # Try to get the courier's partner company
        try:
            partner_company = instance.assigned_courier.courier_profile.partner_company
            if partner_company:
                instance.partner_company = partner_company
        except:
            # If there's an error (e.g., courier profile doesn't exist), just continue
            pass
    
    # If the order has no assigned courier, we might want to clear the partner company
    # But let's keep it for audit purposes
