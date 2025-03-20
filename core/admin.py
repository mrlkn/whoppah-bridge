from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import AuditLogEntry

# Register your models here.

@admin.register(AuditLogEntry)
class AuditLogEntryAdmin(admin.ModelAdmin):
    list_display = ('timestamp', 'user', 'content_type', 'object_repr', 'action', 'ip_address')
    list_filter = ('action', 'timestamp', 'content_type')
    search_fields = ('user__username', 'object_repr', 'object_id')
    date_hierarchy = 'timestamp'
    readonly_fields = ('timestamp', 'user', 'content_type', 'object_id', 'object_repr', 
                       'action', 'changes', 'ip_address', 'user_agent')
    
    fieldsets = (
        (_('Audit Information'), {
            'fields': ('user', 'action', 'timestamp', 'ip_address')
        }),
        (_('Object Information'), {
            'fields': ('content_type', 'object_id', 'object_repr')
        }),
        (_('Changes'), {
            'fields': ('changes',)
        }),
        (_('Additional Information'), {
            'fields': ('user_agent',),
            'classes': ('collapse',)
        }),
    )
    
    def has_add_permission(self, request):
        return False
    
    def has_change_permission(self, request, obj=None):
        return False
    
    def has_delete_permission(self, request, obj=None):
        # Only superusers can delete audit logs
        return request.user.is_superuser
