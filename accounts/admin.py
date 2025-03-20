from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import gettext_lazy as _
from django.db.models import Q
from django.http import HttpResponseRedirect

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
    list_display = ("email", "first_name", "last_name", "user_type", "get_partner_company", "is_staff")
    list_filter = ("user_type", "courier_profile__partner_company", "is_staff", "is_superuser", "is_active", "groups")
    search_fields = ("email", "first_name", "last_name")
    ordering = ("email",)
    
    def get_queryset(self, request):
        """
        Override to filter users based on the partner company of the logged-in user.
        Admin users can see all users, while partner users can only see users from their company.
        """
        qs = super().get_queryset(request)
        
        # Admin can see all users
        if request.user.user_type == 'ADMIN':
            return qs
            
        # Partner company users can only see users from their company
        if request.user.user_type == 'COURIER':
            try:
                partner_company = request.user.courier_profile.partner_company
                # Filter to only show admin users plus users from the same partner company
                return qs.filter(
                    Q(user_type='ADMIN') | 
                    Q(courier_profile__partner_company=partner_company)
                )
            except:
                # If the user has no partner company, only show admin users
                return qs.filter(user_type='ADMIN')
        
        # Default: just return admins
        return qs.filter(user_type='ADMIN')
    
    def get_partner_company(self, obj):
        """Get the partner company for display in the admin list"""
        if obj.user_type == 'COURIER':
            try:
                return obj.courier_profile.get_partner_company_display()
            except:
                return "-"
        return "-"
    get_partner_company.short_description = _("Partner Company")
    
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
    
    def has_add_permission(self, request):
        """Control add permission based on user type and partner company"""
        # Admin can add any user
        if request.user.user_type == 'ADMIN':
            return True
            
        # Partner couriers can only add couriers (for their own company)
        if request.user.user_type == 'COURIER':
            # Check if they have a partner company
            try:
                if request.user.courier_profile.partner_company:
                    return True
            except:
                pass
            
        return False
        
    def has_change_permission(self, request, obj=None):
        """Control change permission based on user type and partner company"""
        # Admin can change any user
        if request.user.user_type == 'ADMIN':
            return True
            
        # No object, check if they can change any
        if obj is None:
            return request.user.user_type == 'COURIER'
            
        # Partner couriers can only change couriers from their company
        if request.user.user_type == 'COURIER' and obj.user_type == 'COURIER':
            try:
                return (request.user.courier_profile.partner_company == 
                       obj.courier_profile.partner_company)
            except:
                pass
                
        return False
    
    def has_delete_permission(self, request, obj=None):
        """Control delete permission based on user type and partner company"""
        # Same logic as change permission
        return self.has_change_permission(request, obj)


@admin.register(CourierProfile)
class CourierProfileAdmin(admin.ModelAdmin):
    """Admin view for CourierProfile"""
    list_display = ("user", "partner_company", "vehicle_type", "availability_status", "service_area")
    list_filter = ("partner_company", "vehicle_type", "availability_status")
    search_fields = ("user__email", "user__first_name", "user__last_name", "service_area")
    readonly_fields = ("created_at", "updated_at")
    
    def get_queryset(self, request):
        """
        Override to filter courier profiles based on the partner company of the logged-in user.
        Admin users can see all courier profiles, while partner users can only see profiles from their company.
        """
        qs = super().get_queryset(request)
        
        # Admin can see all courier profiles
        if request.user.user_type == 'ADMIN':
            return qs
            
        # Partner company users can only see courier profiles from their company
        if request.user.user_type == 'COURIER':
            try:
                partner_company = request.user.courier_profile.partner_company
                return qs.filter(partner_company=partner_company)
            except:
                return qs.none()
        
        # Default: return none
        return qs.none()
        
    def has_add_permission(self, request):
        """Control add permission based on user type"""
        # Only admins can add courier profiles directly (others should use User admin)
        return request.user.user_type == 'ADMIN'
        
    def has_change_permission(self, request, obj=None):
        """Control change permission based on user type and partner company"""
        # Admin can change any courier profile
        if request.user.user_type == 'ADMIN':
            return True
            
        # No object, check if they can change any
        if obj is None:
            return request.user.user_type == 'COURIER'
            
        # Partner couriers can only change courier profiles from their company
        if request.user.user_type == 'COURIER':
            try:
                return request.user.courier_profile.partner_company == obj.partner_company
            except:
                pass
                
        return False
    
    def has_delete_permission(self, request, obj=None):
        """Control delete permission based on user type and partner company"""
        # Only admins can delete courier profiles directly
        return request.user.user_type == 'ADMIN'


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
