from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import gettext_lazy as _

from .models import User, CourierProfile, CustomerProfile


class CourierProfileInline(admin.StackedInline):
    model = CourierProfile
    can_delete = False
    verbose_name_plural = _("Courier Profile")
    fk_name = "user"


class CustomerProfileInline(admin.StackedInline):
    model = CustomerProfile
    can_delete = False
    verbose_name_plural = _("Customer Profile")
    fk_name = "user"


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """Admin view for User"""
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (_("Personal info"), {"fields": ("first_name", "last_name", "phone_number", "address")}),
        (
            _("Permissions"),
            {
                "fields": (
                    "user_type",
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined", "created_at", "updated_at")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "password1", "password2", "user_type"),
            },
        ),
    )
    readonly_fields = ("created_at", "updated_at")
    list_display = ("email", "first_name", "last_name", "user_type", "is_staff")
    list_filter = ("user_type", "is_staff", "is_superuser", "is_active", "groups")
    search_fields = ("email", "first_name", "last_name")
    ordering = ("email",)
    
    def get_inlines(self, request, obj=None):
        if not obj:
            return []
        if obj.user_type == User.Types.COURIER:
            return [CourierProfileInline]
        elif obj.user_type == User.Types.CUSTOMER:
            return [CustomerProfileInline]
        return []
    
    def save_model(self, request, obj, form, change):
        """
        Override save_model to handle group assignment based on user_type
        """
        # First save the user
        super().save_model(request, obj, form, change)
        
        if not change:  # Only for new users
            # Set groups based on user_type
            user_type = obj.user_type
            obj.groups.clear()  # Clear any existing groups
            
            try:
                if user_type == User.Types.ADMIN:
                    admin_group = Group.objects.get(name='Administrators')
                    obj.groups.add(admin_group)
                elif user_type == User.Types.COURIER:
                    courier_group = Group.objects.get(name='Couriers')
                    obj.groups.add(courier_group)
                elif user_type == User.Types.CUSTOMER:
                    customer_group = Group.objects.get(name='Customers')
                    obj.groups.add(customer_group)
            except Group.DoesNotExist:
                # Groups might not exist yet, especially during initial setup
                pass


@admin.register(CourierProfile)
class CourierProfileAdmin(admin.ModelAdmin):
    """Admin view for CourierProfile"""
    list_display = ("user", "vehicle_type", "availability_status", "service_area")
    list_filter = ("vehicle_type", "availability_status")
    search_fields = ("user__email", "user__first_name", "user__last_name", "service_area")
    readonly_fields = ("created_at", "updated_at")


@admin.register(CustomerProfile)
class CustomerProfileAdmin(admin.ModelAdmin):
    """Admin view for CustomerProfile"""
    list_display = ("user", "default_shipping_address")
    search_fields = ("user__email", "user__first_name", "user__last_name")
    readonly_fields = ("created_at", "updated_at")


# Register Groups and Permissions for better admin control
admin.site.unregister(Group)

class GroupAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    filter_horizontal = ('permissions',)
    
    class Meta:
        model = Group
        
admin.site.register(Group, GroupAdmin)
