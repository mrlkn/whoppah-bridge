# Implementation Plan for WhoppahBridge

## Project Setup & Configuration

- [x] Step 1: Initialize Django Project
  - **Task**: Create a new Django project with the basic structure, including virtual environment setup, installing initial dependencies, and configuring project settings.
  - **Files**:
    - `requirements.txt`: Core project dependencies
    - `manage.py`: Django management script
    - `whoppahbridge/settings.py`: Basic project settings
    - `whoppahbridge/urls.py`: URL routing configuration
    - `whoppahbridge/wsgi.py`: WSGI application configuration
    - `whoppahbridge/asgi.py`: ASGI application configuration
    - `.gitignore`: Git ignore rules
    - `README.md`: Project documentation
  - **Step Dependencies**: None
  - **User Instructions**: After code generation, run `pip install -r requirements.txt` to install dependencies and `python manage.py runserver` to test the initial project setup.

- [x] Step 2: Configure Database & Environment Settings
  - **Task**: Set up database connection, environment variables, and configure settings for development and production environments.
  - **Files**:
    - `requirements.txt`: Update with additional database requirements
    - `whoppahbridge/settings.py`: Update with database configuration and environment variables
    - `.env.example`: Template for environment variables
    - `whoppahbridge/settings_dev.py`: Development-specific settings
    - `whoppahbridge/settings_prod.py`: Production-specific settings
  - **Step Dependencies**: Step 1
  - **User Instructions**: Create a `.env` file based on `.env.example` template and set up your local database credentials.

- [x] Step 3: Install and Configure Admin Theme
  - **Task**: Install and configure UnfoldAdmin theme for the Django admin interface.
  - **Files**:
    - `requirements.txt`: Add unfold admin dependencies
    - `whoppahbridge/settings.py`: Configure admin theme
    - `templates/admin/base_site.html`: Customization of the admin interface
    - `static/admin/css/custom.css`: Custom CSS for the admin interface
  - **Step Dependencies**: Step 1
  - **User Instructions**: Run `python manage.py collectstatic` after code generation to collect static files for the admin theme.

## Authentication & User Management

- [x] Step 4: Create User Models
  - **Task**: Extend Django's user model to support different user roles (admin, courier) with appropriate permissions.
  - **Files**:
    - `accounts/models.py`: Custom user model definition
    - `accounts/admin.py`: Admin registration for user models
    - `accounts/apps.py`: App configuration
    - `accounts/__init__.py`: App initialization
    - `accounts/migrations/`: Initial migrations
    - `whoppahbridge/settings.py`: Update with auth user model
  - **Step Dependencies**: Step 1
  - **User Instructions**: After code generation, run `python manage.py makemigrations accounts` and `python manage.py migrate` to create the user tables.

- [x] Step 5: Implement Authentication Views
  - **Task**: Create login, logout, and password reset views with templates for user authentication.
  - **Files**:
    - `accounts/views.py`: Authentication views
    - `accounts/urls.py`: URL patterns for auth views
    - `templates/accounts/login.html`: Login template
    - `templates/accounts/password_reset.html`: Password reset template
    - `templates/accounts/password_reset_done.html`: Password reset done template
    - `templates/accounts/password_reset_confirm.html`: Password reset confirmation template
    - `templates/accounts/password_reset_complete.html`: Password reset complete template
    - `whoppahbridge/urls.py`: Include account URLs
  - **Step Dependencies**: Step 4
  - **User Instructions**: None

- [x] Step 6: Setup Role-Based Access Control
  - **Task**: Implement permission groups and access control for different user roles.
  - **Files**:
    - `accounts/permissions.py`: Permission classes
    - `accounts/middleware.py`: Custom middleware for permission checks
    - `accounts/admin.py`: Update with permission admin
    - `whoppahbridge/settings.py`: Add middleware configuration
  - **Step Dependencies**: Step 4, Step 5
  - **User Instructions**: None

## Core Models & Database Schema

- [x] Step 7: Create Courier Service Models
  - **Task**: Define models for courier services with all necessary fields and relationships.
  - **Files**:
    - `courier/models.py`: Courier service model definition
    - `courier/admin.py`: Admin registration for courier models
    - `courier/apps.py`: App configuration
    - `courier/__init__.py`: App initialization
    - `courier/migrations/`: Initial migrations
    - `whoppahbridge/settings.py`: Update installed apps
  - **Step Dependencies**: Step 4
  - **User Instructions**: After code generation, run `python manage.py makemigrations courier` and `python manage.py migrate` to create the courier tables.

- [x] Step 8: Create Order Models
  - **Task**: Define models for orders, including product details, customer information, and status tracking.
  - **Fields**: Order date	Order ID	Order url	Product url	Product Category	Product name	Weightclass	2 man-delivery	Height	Width	Depth	Seat height	nb_parcels	Pickup customer name	Pickup customer address	Pickup postal code	Pickup city	Pickup country	Pickup e-mail	Pickup phone number	Dropoff customer name	Dropoff customer address	Dropoff post code	Dropoff city	Dropoff country	Dropoff e-mail	Drop-off phone number	Total incl VAT
  - **Context**: Couriers will be able to see orders that are assigned to them and all orders are in different application. This information will be pulled via API later on steps.  
  - **Files**:
    - `orders/models.py`: Order model definitions
    - `orders/admin.py`: Admin registration for order models
    - `orders/apps.py`: App configuration
    - `orders/__init__.py`: App initialization
    - `orders/migrations/`: Initial migrations
    - `whoppahbridge/settings.py`: Update installed apps
  - **Step Dependencies**: Step 7
  - **User Instructions**: After code generation, run `python manage.py makemigrations orders` and `python manage.py migrate` to create the order tables.

- [x] Step 9: Implement Audit Trail Functionality
  - **Task**: Add audit logging functionality to track changes to orders and courier assignments.
  - **Files**:
    - `core/models.py`: Base model with audit fields
    - `core/admin.py`: Admin configuration for audit display
    - `core/apps.py`: App configuration
    - `core/__init__.py`: App initialization
    - `core/middleware.py`: Audit logging middleware
    - `orders/models.py`: Update with audit mixin
    - `whoppahbridge/settings.py`: Update middleware configuration
  - **Step Dependencies**: Step 8
  - **User Instructions**: After code generation, run `python manage.py makemigrations core` and `python manage.py migrate` to create the audit tables.

## Admin Interface

- [x] Step 10: Customize Admin for Order Management
  - **Task**: Create a custom admin interface for order management with filtering, search, and bulk actions.
  - **Files**:
    - `orders/admin.py`: Enhanced order admin interface
    - `templates/admin/orders/order/change_list.html`: Custom order list template
    - `templates/admin/orders/order/change_form.html`: Custom order detail template
    - `static/admin/js/order_admin.js`: JavaScript for enhanced admin functionality
  - **Step Dependencies**: Step 8, Step 3
  - **User Instructions**: None

- [x] Step 11: Implement Courier Service Admin
  - **Task**: Create admin interface for managing courier services with proper permissions.
  - **Files**:
    - `courier/admin.py`: Enhanced courier admin interface
    - `templates/admin/courier/courierservice/change_list.html`: Custom courier list template
    - `templates/admin/courier/courierservice/change_form.html`: Custom courier detail template
  - **Step Dependencies**: Step 7, Step 3
  - **User Instructions**: None

- [x] Step 12: Develop Admin Dashboard
  - **Task**: Create a custom admin dashboard with analytics, metrics, and quick actions.
  - **Files**:
    - `core/views.py`: Admin dashboard view
    - `core/urls.py`: URL configuration for admin dashboard
    - `templates/admin/dashboard.html`: Dashboard template
    - `static/admin/js/dashboard.js`: Dashboard JavaScript functionality
    - `static/admin/css/dashboard.css`: Dashboard styling
    - `whoppahbridge/urls.py`: Update with dashboard URL
  - **Step Dependencies**: Step 10, Step 11
  - **User Instructions**: None

# WhoppahBridge Adjusted Implementation Plan

## API Integration

- [ ] Step 13: Create Whoppah CMS API Client
  - **Task**: Implement a client for connecting to the Whoppah CMS API to fetch order data
  - **Files**:
    - `integration/api_client.py`: API client with authentication and request handling
    - `integration/exceptions.py`: Custom exceptions for API errors
    - `integration/models.py`: Any models needed for API configuration
    - `integration/apps.py` & `integration/__init__.py`: App configuration
  - **Step Dependencies**: Step 8
  - **User Instructions**: Update `.env` file with Whoppah CMS API credentials
  - **Implementation Notes**: Ensure compatibility with the existing Order model structure

- [ ] Step 14: Implement Order Synchronization
  - **Task**: Create functionality to synchronize orders between Whoppah CMS and WhoppahBridge
  - **Files**:
    - `integration/sync.py`: Logic to map API data to Order models
    - `integration/management/commands/sync_orders.py`: CLI command for sync
    - `integration/tasks.py`: Background tasks for automatic synchronization
  - **Step Dependencies**: Step 13
  - **User Instructions**: After code generation, test the sync with `python manage.py sync_orders`
  - **Implementation Notes**: Leverage the audit trail for tracking sync operations

- [ ] Step 15: Setup Webhook Handlers
  - **Task**: Implement webhook endpoints for real-time updates
  - **Files**: 
    - `integration/webhooks.py`: Webhook handlers
    - `integration/urls.py`: Webhook URL routing
    - `whoppahbridge/urls.py`: Include webhook URLs
  - **Step Dependencies**: Step 14
  - **User Instructions**: Share the webhook URL with Whoppah CMS for configuration
  - **Implementation Notes**: Ensure webhooks properly update related models and trigger audit logging

## Courier Dashboard

- [ ] Step 16: Create Base Templates and Layout
  - **Task**: Develop base templates for the courier dashboard
  - **Files**:
    - `templates/base.html`: Base template with common elements
    - `templates/dashboard/base.html`: Dashboard-specific base template
    - `static/css/main.css`: Main application styling
    - `static/js/main.js`: Common JavaScript functionality
    - `static/css/dashboard.css`: Dashboard-specific styling
  - **Step Dependencies**: Step 6
  - **User Instructions**: None
  - **Implementation Notes**: Use the UnfoldAdmin theme styling for consistency

- [ ] Step 17: Implement Courier Dashboard Views
  - **Task**: Create the courier-specific dashboard views
  - **Files**:
    - `dashboard/views.py`: Views limited to courier-assigned orders
    - `dashboard/urls.py`: URL patterns for dashboard
    - `dashboard/apps.py`: App configuration
    - `dashboard/__init__.py`: App initialization
    - `templates/dashboard/index.html`: Dashboard homepage template
    - `templates/dashboard/orders/list.html`: Order list template
    - `static/js/dashboard/filters.js`: Order filtering functionality
    - `whoppahbridge/urls.py`: Include dashboard URLs
  - **Step Dependencies**: Step 16, Step 8
  - **User Instructions**: None
  - **Implementation Notes**: Utilize the User.is_courier property for authentication

- [ ] Step 18: Implement Order Detail View
  - **Task**: Create detailed order view for couriers
  - **Files**:
    - `dashboard/views.py`: Add order detail view
    - `templates/dashboard/orders/detail.html`: Order detail template
    - `static/js/dashboard/order-detail.js`: Order detail functionality
    - `static/css/dashboard/order-detail.css`: Order detail styling
  - **Step Dependencies**: Step 17
  - **User Instructions**: None
  - **Implementation Notes**: Ensure address and product details are displayed clearly

- [ ] Step 19: Add Status Update Functionality
  - **Task**: Allow couriers to update order status
  - **Files**:
    - `orders/views.py`: Status update view
    - `orders/urls.py`: URL configuration for status updates
    - `templates/dashboard/orders/status_update.html`: Status update modal template
    - `static/js/dashboard/status-update.js`: Status update JavaScript
    - `whoppahbridge/urls.py`: Include order update URLs
  - **Step Dependencies**: Step 18
  - **User Instructions**: None
  - **Implementation Notes**: Integrate with the existing audit trail functionality

- [ ] Step 20: Implement Order History and Tracking
  - **Task**: Show order history using the audit data
  - **Files**:
    - `dashboard/views.py`: Add history view
    - `templates/dashboard/orders/history.html`: Order history template
    - `static/js/dashboard/history.js`: History view JavaScript
  - **Step Dependencies**: Step 19, Step 9
  - **User Instructions**: None
  - **Implementation Notes**: Utilize the existing AuditLogEntry model

## Super Admin Features

- [ ] Step 21: Create Order Assignment Interface
  - **Task**: Implement order assignment to couriers
  - **Files**:
    - `admin_dashboard/views.py`: Order assignment views
    - `admin_dashboard/urls.py`: URL patterns for admin features
    - `admin_dashboard/apps.py`: App configuration
    - `admin_dashboard/__init__.py`: App initialization
    - `templates/admin_dashboard/order_assignment.html`: Assignment template
    - `static/js/admin_dashboard/assignment.js`: Assignment JavaScript
    - `whoppahbridge/urls.py`: Include admin dashboard URLs
  - **Step Dependencies**: Step 12, Step 8, Step 7
  - **User Instructions**: None
  - **Implementation Notes**: Use the existing User model with COURIER type filtering

- [ ] Step 22: Enhance Analytics and Reporting
  - **Task**: Expand the dashboard analytics
  - **Files**:
    - `admin_dashboard/views.py`: Add analytics views
    - `admin_dashboard/reports.py`: Report generation functions
    - `templates/admin_dashboard/analytics.html`: Analytics dashboard template
    - `templates/admin_dashboard/reports.html`: Reports template
    - `static/js/admin_dashboard/charts.js`: Charting JavaScript
    - `static/css/admin_dashboard/reports.css`: Report styling
  - **Step Dependencies**: Step 21
  - **User Instructions**: None
  - **Implementation Notes**: Build on the existing core/views.py dashboard

## Mobile Responsiveness & User Experience

- [ ] Step 23: Implement Responsive Design
  - **Task**: Ensure mobile compatibility
  - **Files**:
    - `static/css/responsive.css`: Responsive CSS rules
    - `templates/base.html`: Update with responsive meta tags
    - `static/js/mobile.js`: Mobile-specific JavaScript
    - Update all dashboard templates with responsive classes
  - **Step Dependencies**: Step 16, Step 17, Step 18, Step 19
  - **User Instructions**: None
  - **Implementation Notes**: Utilize the existing UnfoldAdmin responsive features

## Notification System

- [ ] Step 24: Implement Email Notification System
  - **Task**: Set up the notification infrastructure
  - **Files**:
    - `notifications/email.py`: Email sending functions
    - `notifications/apps.py`: App configuration
    - `notifications/__init__.py`: App initialization
    - `templates/emails/base_email.html`: Base email template
    - `whoppahbridge/settings.py`: Update with email configuration
  - **Step Dependencies**: Step 8
  - **User Instructions**: Configure email settings in the `.env` file
  - **Implementation Notes**: Configure with the existing settings structure

- [ ] Step 25: Add Order Status Notifications
  - **Task**: Send notifications for order status changes
  - **Files**:
    - `notifications/handlers.py`: Event handlers for notifications
    - `templates/emails/status_update.html`: Status update email template
    - `orders/views.py`: Update to trigger notifications
    - `notifications/management/commands/send_reminders.py`: Command for sending reminders
  - **Step Dependencies**: Step 24, Step 19
  - **User Instructions**: Set up a cron job to run `python manage.py send_reminders` daily if needed
  - **Implementation Notes**: Integrate with the audit trail to trigger notifications

## Testing & Documentation

- [ ] Step 26: Create Comprehensive Tests
  - **Task**: Implement tests for all functionality
  - **Files**:
    - `accounts/tests.py`: Tests for user authentication
    - `orders/tests.py`: Tests for order models and functions
    - `integration/tests.py`: Tests for API integration
    - `dashboard/tests.py`: Tests for dashboard views
    - `tests/integration/test_workflows.py`: Workflow integration tests
  - **Step Dependencies**: All implementation steps
  - **User Instructions**: Run tests with `python manage.py test`
  - **Implementation Notes**: Focus on the API integration and courier dashboard

- [ ] Step 27: Develop User Documentation
  - **Task**: Create documentation for couriers and administrators
  - **Files**:
    - `docs/user/courier_guide.md`: Courier user guide
    - `docs/user/admin_guide.md`: Administrator guide
    - `docs/user/images/`: Screenshots and illustrations
    - `templates/dashboard/help.html`: In-app help page
  - **Step Dependencies**: All implementation steps
  - **User Instructions**: None
  - **Implementation Notes**: Include details about the different user types and permissions

- [ ] Step 28: Finalize Deployment Configuration
  - **Task**: Prepare for production deployment
  - **Files**:
    - `whoppahbridge/settings_prod.py`: Update production settings
    - `requirements_prod.txt`: Production dependencies
    - `wsgi.py`: Production WSGI configuration
    - `.env.production.example`: Production environment template
    - `docs/technical/deployment.md`: Deployment guide
  - **Step Dependencies**: All implementation steps
  - **User Instructions**: Deploy using the instructions in `docs/technical/deployment.md`
  - **Implementation Notes**: Build on the existing settings_prod.py configurations