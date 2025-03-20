import threading
import inspect
from django.utils.deprecation import MiddlewareMixin
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.apps import apps
from django.contrib.contenttypes.models import ContentType
from .models import AuditLogEntry, AuditableMixin

# Thread-local storage for tracking the user and request
_thread_locals = threading.local()

def get_current_user():
    """Return the current user from thread-local storage"""
    return getattr(_thread_locals, 'user', None)

def get_current_request():
    """Return the current request from thread-local storage"""
    return getattr(_thread_locals, 'request', None)

class AuditMiddleware(MiddlewareMixin):
    """
    Middleware that adds the request and authenticated user to thread local storage
    """
    def process_request(self, request):
        """Store request and user in thread local storage"""
        _thread_locals.request = request
        _thread_locals.user = request.user if request.user.is_authenticated else None
    
    def process_response(self, request, response):
        """Clean up thread local storage"""
        if hasattr(_thread_locals, 'request'):
            del _thread_locals.request
        if hasattr(_thread_locals, 'user'):
            del _thread_locals.user
        return response


@receiver(post_save)
def audit_post_save(sender, instance, created, **kwargs):
    """Create audit log for model save events"""
    if not issubclass(sender, AuditableMixin):
        return
    
    # Skip if this is a direct call from audit_log_entry itself to avoid recursion
    calling_frame = inspect.currentframe().f_back
    if calling_frame and 'audit_log_entry' in calling_frame.f_code.co_name:
        return
    
    request = get_current_request()
    user = get_current_user()
    
    # Get IP address and user agent
    ip_address = None
    user_agent = ""
    if request:
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip_address = x_forwarded_for.split(',')[0].strip()
        else:
            ip_address = request.META.get('REMOTE_ADDR')
        user_agent = request.META.get('HTTP_USER_AGENT', '')
    
    # Create the audit log entry
    action = 'CREATE' if created else 'UPDATE'
    changes = instance.get_changes()
    
    AuditLogEntry.objects.create(
        user=user,
        content_type=instance.__class__.__name__,
        object_id=str(instance.pk),
        object_repr=str(instance),
        action=action,
        changes=changes,
        ip_address=ip_address,
        user_agent=user_agent
    )
    
    # Set created_by and updated_by
    if created and user and not instance.created_by:
        instance.created_by = user
    if user:
        instance.updated_by = user
    
    # Save the instance without triggering the signal again
    if user and (created and not instance.created_by or not created):
        post_save.disconnect(audit_post_save, sender=sender)
        instance.save()
        post_save.connect(audit_post_save, sender=sender)


@receiver(post_delete)
def audit_post_delete(sender, instance, **kwargs):
    """Create audit log for model delete events"""
    if not issubclass(sender, AuditableMixin):
        return
    
    request = get_current_request()
    user = get_current_user()
    
    # Get IP address and user agent
    ip_address = None
    user_agent = ""
    if request:
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip_address = x_forwarded_for.split(',')[0].strip()
        else:
            ip_address = request.META.get('REMOTE_ADDR')
        user_agent = request.META.get('HTTP_USER_AGENT', '')
    
    # Create the audit log entry
    AuditLogEntry.objects.create(
        user=user,
        content_type=instance.__class__.__name__,
        object_id=str(instance.pk),
        object_repr=str(instance),
        action='DELETE',
        changes={},
        ip_address=ip_address,
        user_agent=user_agent
    )
