from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from accounts.models import User, CourierProfile, CustomerProfile
from accounts.permissions import create_default_groups

class Command(BaseCommand):
    help = 'Set up default user groups and permissions for role-based access control'

    def handle(self, *args, **options):
        self.stdout.write(self.style.MIGRATE_HEADING('Creating default user groups and permissions...'))
        
        # Call the function from permissions.py to create the default groups
        create_default_groups()
        
        # Add basic model permissions for existing models
        self.setup_model_permissions()
        
        self.stdout.write(self.style.SUCCESS('Successfully created default groups and permissions'))
    
    def setup_model_permissions(self):
        """Set up model permissions for existing models."""
        # Get groups
        try:
            admin_group = Group.objects.get(name='Administrators')
            courier_group = Group.objects.get(name='Couriers')
            customer_group = Group.objects.get(name='Customers')
        except Group.DoesNotExist:
            self.stdout.write(self.style.ERROR('Groups do not exist. Run create_default_groups first.'))
            return
        
        # User model permissions
        user_content_type = ContentType.objects.get_for_model(User)
        user_permissions = Permission.objects.filter(content_type=user_content_type)
        
        # CourierProfile permissions
        courier_profile_content_type = ContentType.objects.get_for_model(CourierProfile)
        courier_profile_permissions = Permission.objects.filter(content_type=courier_profile_content_type)
        
        # CustomerProfile permissions
        customer_profile_content_type = ContentType.objects.get_for_model(CustomerProfile)
        customer_profile_permissions = Permission.objects.filter(content_type=customer_profile_content_type)
        
        # Assign permissions to admin group - admins can do everything
        for permission in list(user_permissions) + list(courier_profile_permissions) + list(customer_profile_permissions):
            admin_group.permissions.add(permission)
        
        # Courier permissions
        # Couriers can view but not edit user profiles, can manage their own courier profile
        courier_group.permissions.add(*Permission.objects.filter(
            content_type=user_content_type, 
            codename__in=['view_user']
        ))
        
        courier_group.permissions.add(*Permission.objects.filter(
            content_type=courier_profile_content_type,
            codename__in=['view_courierprofile', 'change_courierprofile']
        ))
        
        # Customer permissions
        # Customers can view but not edit user profiles, can manage their own customer profile
        customer_group.permissions.add(*Permission.objects.filter(
            content_type=user_content_type,
            codename__in=['view_user']
        ))
        
        customer_group.permissions.add(*Permission.objects.filter(
            content_type=customer_profile_content_type,
            codename__in=['view_customerprofile', 'change_customerprofile']
        ))
        
        self.stdout.write(self.style.SUCCESS('Model permissions assigned successfully'))
