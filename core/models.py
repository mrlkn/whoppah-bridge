from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
import json

class AuditLogEntry(models.Model):
    """
    Model to store audit log entries for tracked models
    """
    ACTION_TYPES = (
        ('CREATE', _('Create')),
        ('UPDATE', _('Update')),
        ('DELETE', _('Delete')),
    )
    
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='audit_logs',
        verbose_name=_('User')
    )
    content_type = models.CharField(_('Content Type'), max_length=100)
    object_id = models.CharField(_('Object ID'), max_length=50)
    object_repr = models.CharField(_('Object Representation'), max_length=255)
    action = models.CharField(_('Action'), max_length=10, choices=ACTION_TYPES)
    changes = models.JSONField(_('Changes'), default=dict)
    timestamp = models.DateTimeField(_('Timestamp'), auto_now_add=True)
    ip_address = models.GenericIPAddressField(_('IP Address'), null=True, blank=True)
    user_agent = models.TextField(_('User Agent'), blank=True)
    
    class Meta:
        verbose_name = _('Audit Log Entry')
        verbose_name_plural = _('Audit Log Entries')
        ordering = ['-timestamp']
    
    def __str__(self):
        return f"{self.get_action_display()} {self.object_repr} by {self.user}"


class AuditableMixin(models.Model):
    """
    Abstract base model that provides audit fields
    """
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='%(app_label)s_%(class)s_created',
        verbose_name=_('Created By')
    )
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='%(app_label)s_%(class)s_updated',
        verbose_name=_('Updated By')
    )
    created_at = models.DateTimeField(_('Created At'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Updated At'), auto_now=True)
    
    class Meta:
        abstract = True
    
    def get_changes(self, old_instance=None):
        """Get a dictionary of changed fields with old and new values"""
        if not old_instance:
            # For new instances, return all fields
            return {
                field.name: {
                    'old': None,
                    'new': getattr(self, field.name)
                } for field in self._meta.fields
                if not field.name.endswith('_ptr') and field.name not in ['created_at', 'updated_at']
            }
        
        changes = {}
        for field in self._meta.fields:
            if field.name.endswith('_ptr') or field.name in ['created_at', 'updated_at']:
                continue
                
            old_value = getattr(old_instance, field.name)
            new_value = getattr(self, field.name)
            
            # Handle special cases like ForeignKey
            if field.is_relation:
                old_value = str(old_value) if old_value else None
                new_value = str(new_value) if new_value else None
            
            if old_value != new_value:
                changes[field.name] = {
                    'old': old_value,
                    'new': new_value
                }
        
        return changes
