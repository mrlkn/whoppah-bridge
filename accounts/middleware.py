from django.shortcuts import redirect
from django.urls import reverse, resolve
from django.contrib import messages
from django.http import HttpResponseForbidden


class RoleBasedAccessMiddleware:
    """
    Middleware to enforce role-based access control.
    Restricts access to views based on user's type (Admin, Courier, Customer).
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
        
    def __call__(self, request):
        if not request.user.is_authenticated:
            # For unauthenticated users, let Django's auth middleware handle it
            return self.get_response(request)
        
        # Admin users have access to everything
        if request.user.user_type == 'ADMIN':
            return self.get_response(request)
        
        # Get current URL path
        path = request.path_info
        
        # Paths that start with /admin/ are restricted to admin users only
        if path.startswith('/admin/') and not request.user.is_staff:
            messages.error(request, "You don't have permission to access the admin area.")
            return redirect('accounts:login')
        
        # Courier-specific sections will be added in Step 7
        # if path.startswith('/courier/') and not request.user.user_type == 'COURIER':
        #     return HttpResponseForbidden("You don't have permission to access courier resources.")
        
        # Customer-specific sections will be added in Step 8
        # if path.startswith('/customer/') and not request.user.user_type == 'CUSTOMER':
        #     return HttpResponseForbidden("You don't have permission to access customer resources.")
        
        # Allow the request to proceed
        return self.get_response(request)


class PartnerCompanyMiddleware:
    """
    Middleware to enforce partner company access control.
    This middleware ensures partner company users can only access their own resources.
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
        
    def __call__(self, request):
        # Skip for unauthenticated users or admin users
        if not request.user.is_authenticated or request.user.user_type == 'ADMIN':
            return self.get_response(request)
            
        # Skip for non-courier users (they don't belong to partner companies)
        if request.user.user_type != 'COURIER':
            return self.get_response(request)
            
        # Get partner company for the user
        try:
            partner_company = request.user.courier_profile.partner_company
            
            # Set partner company on request for use in views
            request.partner_company = partner_company
        except:
            # If there's no courier profile or partner company, just continue
            pass
            
        # Allow the request to proceed - actual filtering will be done at the queryset level
        return self.get_response(request)


class ActivityTrackingMiddleware:
    """
    Middleware to track user activity.
    Records when users last accessed the application.
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
        
    def __call__(self, request):
        response = self.get_response(request)
        
        # Update last activity timestamp for authenticated users
        # Skip for AJAX requests and static/media files
        if (request.user.is_authenticated and 
            not request.headers.get('x-requested-with') == 'XMLHttpRequest' and
            not request.path.startswith(('/static/', '/media/'))):
            
            # Update user's last activity timestamp
            # This will be implemented when we update the User model in future steps
            # request.user.update_last_activity()
            pass
            
        return response
