from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from rest_framework import permissions


def create_default_groups():
    """Create default groups with appropriate permissions."""
    # Admin Group
    admin_group, _ = Group.objects.get_or_create(name='Administrators')
    
    # Courier Group
    courier_group, _ = Group.objects.get_or_create(name='Couriers')
    
    # Customer Group
    customer_group, _ = Group.objects.get_or_create(name='Customers')
    
    # Add permissions to groups
    
    # Clear existing permissions to avoid duplicates
    admin_group.permissions.clear()
    courier_group.permissions.clear()
    customer_group.permissions.clear()
    
    # Add model permissions based on content types
    # The specific permissions will be expanded when the actual models are created
    # This is a placeholder for future models
    
    # Admin permissions - can do everything
    # We'll add all permissions once the models are fully defined in future steps
    
    # Courier permissions - can view and update their assigned deliveries/orders
    # These will be expanded in Step 7 & 8 when courier and order models are defined

    # Customer permissions - can view and manage their orders
    # These will be expanded in Step 8 when order models are defined


class IsAdmin(permissions.BasePermission):
    """
    Permission class to check if user is an Admin.
    """
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.user_type == 'ADMIN')


class IsCourier(permissions.BasePermission):
    """
    Permission class to check if user is a Courier.
    """
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.user_type == 'COURIER')


class IsCustomer(permissions.BasePermission):
    """
    Permission class to check if user is a Customer.
    """
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.user_type == 'CUSTOMER')


class IsOwnerOrAdmin(permissions.BasePermission):
    """
    Permission class to check if user is the owner of an object or an admin.
    Requires the object to have a 'user' attribute that can be compared with request.user
    """
    def has_object_permission(self, request, view, obj):
        # Admin can access any object
        if request.user.user_type == 'ADMIN':
            return True
        
        # Check if object has user attribute and it matches the request user
        return hasattr(obj, 'user') and obj.user == request.user
