import json
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.contrib.auth.models import AnonymousUser
from django.utils.translation import gettext_lazy as _

from .models import AuditLogEntry
from orders.models import Order, PickupAddress, DropoffAddress, OrderNote

import threading
_thread_locals = threading.local()

def get_current_user():
    """Get the current user from thread local storage"""
    return getattr(_thread_locals, 'user', None)

def get_current_request():
    """Get the current request from thread local storage"""
    return getattr(_thread_locals, 'request', None)

@receiver(post_save, sender=Order)
@receiver(post_save, sender=PickupAddress)
@receiver(post_save, sender=DropoffAddress)
@receiver(post_save, sender=OrderNote)
def log_save(sender, instance, created, **kwargs):
    """Log when an instance is created or updated"""
    # Get current user and request
    user = get_current_user()
    request = get_current_request()
    
    # Skip anonymous users and no request
    if isinstance(user, AnonymousUser) or user is None:
        return
    
    # Get IP address and user agent
    ip_address = None
    user_agent = None
    if request:
        ip_address = request.META.get('REMOTE_ADDR')
        user_agent = request.META.get('HTTP_USER_AGENT', '')
    
    # Get model changes
    if created:
        action = 'CREATE'
        changes = instance.get_changes() if hasattr(instance, 'get_changes') else {}
    else:
        action = 'UPDATE'
        # We don't have the old instance here, so we'll just log what we know
        changes = instance.get_changes() if hasattr(instance, 'get_changes') else {}
    
    # Create audit log entry
    AuditLogEntry.objects.create(
        user=user,
        content_type=sender.__name__,
        object_id=str(instance.pk),
        object_repr=str(instance),
        action=action,
        changes=changes,
        ip_address=ip_address,
        user_agent=user_agent
    )

@receiver(post_delete, sender=Order)
@receiver(post_delete, sender=PickupAddress)
@receiver(post_delete, sender=DropoffAddress)
@receiver(post_delete, sender=OrderNote)
def log_delete(sender, instance, **kwargs):
    """Log when an instance is deleted"""
    # Get current user and request
    user = get_current_user()
    request = get_current_request()
    
    # Skip anonymous users and no request
    if isinstance(user, AnonymousUser) or user is None:
        return
    
    # Get IP address and user agent
    ip_address = None
    user_agent = None
    if request:
        ip_address = request.META.get('REMOTE_ADDR')
        user_agent = request.META.get('HTTP_USER_AGENT', '')
    
    # Create audit log entry
    AuditLogEntry.objects.create(
        user=user,
        content_type=sender.__name__,
        object_id=str(instance.pk),
        object_repr=str(instance),
        action='DELETE',
        changes={},  # We don't have the changes here
        ip_address=ip_address,
        user_agent=user_agent
    )
