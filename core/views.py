from django.contrib.auth.forms import User
from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Count, Sum, Q
from django.utils import timezone
from datetime import timedelta
from django.urls import reverse
from orders.models import Order, OrderState
from accounts.models import CourierProfile

# Create your views here.

@staff_member_required
def admin_dashboard(request):
    """
    Admin dashboard view showing key metrics and analytics.
    """
    # Get current date and date ranges for metrics
    today = timezone.now().date()
    week_ago = today - timedelta(days=7)
    month_ago = today - timedelta(days=30)
    
    # Orders metrics
    total_orders = Order.objects.count()
    new_orders = Order.objects.filter(status=OrderState.NEW).count()
    orders_in_progress = Order.objects.filter(status=OrderState.SHIPPED).count()
    orders_delivered = Order.objects.filter(status=OrderState.DELIVERED).count()
    
    # Weekly orders data
    last_week_orders = Order.objects.filter(created_at__date__gte=week_ago)
    orders_last_week = last_week_orders.count()
    
    # Orders by status
    orders_by_status = Order.objects.values('status').annotate(count=Count('id')).order_by('-count')
    
    # Orders without courier
    unassigned_orders = Order.objects.filter(assigned_courier__isnull=True).count()
    
    # Orders by city (top 5)
    orders_by_pickup_city = Order.objects.values('pickup_address__city').annotate(
        count=Count('id')).order_by('-count')[:5]
    
    orders_by_dropoff_city = Order.objects.values('dropoff_address__city').annotate(
        count=Count('id')).order_by('-count')[:5]
    
    # Orders requiring 2-man delivery
    two_man_delivery_orders = Order.objects.filter(two_man_delivery=True).count()
    
    # Courier metrics
    total_couriers = CourierProfile.objects.count()
    active_couriers = CourierProfile.objects.count()
    
    # Orders by weight class
    orders_by_weight = Order.objects.values('weight_class').annotate(count=Count('id')).order_by('-count')
    
    # Recent orders
    recent_orders = Order.objects.all().order_by('-created_at')[:5]
    
    # Quick actions
    quick_actions = [
        {
            'name': 'View All Orders',
            'url': reverse('admin:orders_order_changelist'),
            'icon': 'fa-list-alt',
            'color': 'primary'
        },
        {
            'name': 'Add New Order',
            'url': reverse('admin:orders_order_add'),
            'icon': 'fa-plus-circle',
            'color': 'success'
        },
        {
            'name': 'Manage Couriers',
            'url': reverse('admin:accounts_courierprofile_changelist'),
            'icon': 'fa-truck',
            'color': 'info'
        },
        {
            'name': 'View Audit Log',
            'url': reverse('admin:core_auditlogentry_changelist'),
            'icon': 'fa-history',
            'color': 'secondary'
        },
    ]
    
    # Daily order counts for the last 7 days
    daily_order_data = []
    for i in range(7, 0, -1):
        day = today - timedelta(days=i - 1)
        count = Order.objects.filter(created_at__date=day).count()
        daily_order_data.append({
            'date': day.strftime('%Y-%m-%d'),
            'label': day.strftime('%a'),
            'count': count
        })
    
    context = {
        'total_orders': total_orders,
        'new_orders': new_orders,
        'orders_in_progress': orders_in_progress,
        'orders_delivered': orders_delivered,
        'orders_last_week': orders_last_week,
        'unassigned_orders': unassigned_orders,
        'orders_by_status': orders_by_status,
        'orders_by_pickup_city': orders_by_pickup_city,
        'orders_by_dropoff_city': orders_by_dropoff_city,
        'two_man_delivery_orders': two_man_delivery_orders,
        'total_couriers': total_couriers,
        'active_couriers': active_couriers,
        'orders_by_weight': orders_by_weight,
        'recent_orders': recent_orders,
        'quick_actions': quick_actions,
        'daily_order_data': daily_order_data,
        'title': 'Dashboard',
    }
    
    return render(request, 'admin/dashboard.html', context)
