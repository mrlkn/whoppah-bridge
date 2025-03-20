from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django.urls import path
from django.http import HttpResponse
from django.template.response import TemplateResponse
from django.utils.html import format_html
from django.contrib.admin import SimpleListFilter
from django.db.models import Q
import csv
from datetime import datetime
from .models import Order, PickupAddress, DropoffAddress, OrderNote, OrderState

class WeightFilter(SimpleListFilter):
    title = _('Weight')
    parameter_name = 'weight'
    
    def lookups(self, request, model_admin):
        return (
            ('light', _('Light (0-5kg)')),
            ('medium', _('Medium (5-20kg)')),
            ('heavy', _('Heavy (20-50kg)')),
            ('very_heavy', _('Very Heavy (50kg+)')),
        )
    
    def queryset(self, request, queryset):
        if self.value() == 'light':
            return queryset.filter(weight__lte=5)
        if self.value() == 'medium':
            return queryset.filter(weight__gt=5, weight__lte=20)
        if self.value() == 'heavy':
            return queryset.filter(weight__gt=20, weight__lte=50)
        if self.value() == 'very_heavy':
            return queryset.filter(weight__gt=50)
        return queryset

class TwoManDeliveryFilter(SimpleListFilter):
    title = _('2-Man Delivery')
    parameter_name = 'two_man_delivery'
    
    def lookups(self, request, model_admin):
        return (
            ('yes', _('Required')),
            ('no', _('Not Required')),
        )
    
    def queryset(self, request, queryset):
        if self.value() == 'yes':
            return queryset.filter(two_man_delivery=True)
        if self.value() == 'no':
            return queryset.filter(two_man_delivery=False)
        return queryset

class CourierFilter(SimpleListFilter):
    title = _('Courier Assignment')
    parameter_name = 'courier'
    
    def lookups(self, request, model_admin):
        return (
            ('assigned', _('Assigned')),
            ('unassigned', _('Unassigned')),
        )
    
    def queryset(self, request, queryset):
        if self.value() == 'assigned':
            return queryset.filter(assigned_courier__isnull=False)
        if self.value() == 'unassigned':
            return queryset.filter(assigned_courier__isnull=True)
        return queryset

class PickupAddressInline(admin.StackedInline):
    model = PickupAddress
    can_delete = False
    fields = ('customer_name', 'address', 'postal_code', 'city', 'country', 'phone_number', 'email')
    readonly_fields = ('created_by', 'updated_by', 'created_at', 'updated_at')
    extra = 0
    verbose_name_plural = _('Pickup Address')
    ordering_field = None

class DropoffAddressInline(admin.StackedInline):
    model = DropoffAddress
    can_delete = False
    fields = ('customer_name', 'address', 'postal_code', 'city', 'country', 'phone_number', 'email')
    readonly_fields = ('created_by', 'updated_by', 'created_at', 'updated_at')
    extra = 0
    verbose_name_plural = _('Dropoff Address')
    ordering_field = None

class OrderNoteInline(admin.TabularInline):
    model = OrderNote
    extra = 1
    fields = ('content', 'created_by', 'created_at')
    readonly_fields = ('created_by', 'created_at')
    verbose_name_plural = _('Order Notes')
    ordering_field = None

    def has_change_permission(self, request, obj=None):
        return False

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_id', 'product_name_display', 'order_date', 'status_badge', 'weight_display', 
                    'assigned_courier_display', 'pickup_city', 'dropoff_city', 'two_man_delivery_icon')
    list_filter = ('status', 'order_date', WeightFilter, TwoManDeliveryFilter, CourierFilter)
    search_fields = ('order_id', 'product_name', 'pickup_address__customer_name', 'pickup_address__city',
                     'dropoff_address__customer_name', 'dropoff_address__city')
    date_hierarchy = 'order_date'
    list_per_page = 25
    actions = ['export_as_csv', 'mark_as_accepted', 'mark_as_shipped', 'mark_as_delivered', 'mark_as_canceled']
    
    fieldsets = (
        (_('Order Information'), {
            'fields': ('order_id', 'order_date', 'order_url', 'status', 'assigned_courier')
        }),
        (_('Product Information'), {
            'fields': ('product_name', 'product_category', 'product_url', 'weight', 'two_man_delivery')
        }),
        (_('Product Dimensions'), {
            'fields': ('height', 'width', 'depth', 'seat_height')
        }),
        (_('Delivery Information'), {
            'fields': ('number_of_parcels', 'total_price')
        }),
        (_('Audit Information'), {
            'fields': ('created_by', 'created_at', 'updated_by', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ('created_by', 'created_at', 'updated_by', 'updated_at')
    inlines = [PickupAddressInline, DropoffAddressInline, OrderNoteInline]
    save_on_top = True
    
    class Media:
        js = ('admin/js/order_admin.js',)
    
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('order-statistics/', self.admin_site.admin_view(self.order_statistics_view), name='order-statistics'),
        ]
        return custom_urls + urls
    
    def order_statistics_view(self, request):
        context = {
            **self.admin_site.each_context(request),
            'title': _('Order Statistics'),
            'orders_by_status': self._get_orders_by_status(),
            'orders_by_weight': self._get_orders_by_weight(),
            'two_man_delivery_count': Order.objects.filter(two_man_delivery=True).count(),
            'opts': self.model._meta,
        }
        return TemplateResponse(request, 'admin/orders/order/order_statistics.html', context)
    
    def _get_orders_by_status(self):
        result = {}
        for status_code, status_name in OrderState.CHOICES:
            result[status_name] = Order.objects.filter(status=status_code).count()
        return result
    
    def _get_orders_by_weight(self):
        result = {
            _('Light (0-5kg)'): Order.objects.filter(weight__lte=5).count(),
            _('Medium (5-20kg)'): Order.objects.filter(weight__gt=5, weight__lte=20).count(),
            _('Heavy (20-50kg)'): Order.objects.filter(weight__gt=20, weight__lte=50).count(),
            _('Very Heavy (50kg+)'): Order.objects.filter(weight__gt=50).count(),
        }
        return result
    
    def product_name_display(self, obj):
        if obj.product_url:
            return format_html('<a href="{}" target="_blank">{}</a>', obj.product_url, obj.product_name)
        return obj.product_name
    product_name_display.short_description = _('Product')
    product_name_display.admin_order_field = 'product_name'
    
    def weight_display(self, obj):
        if obj.weight is not None:
            return f"{obj.weight} kg"
        return "-"
    weight_display.short_description = _('Weight')
    weight_display.admin_order_field = 'weight'
    
    def status_badge(self, obj):
        status_colors = {
            'new': 'primary',
            'accepted': 'info',
            'shipped': 'warning',
            'delivered': 'success',
            'canceled': 'danger',
            'expired': 'secondary',
            'disputed': 'danger',
            'completed': 'success',
        }
        color = status_colors.get(obj.status, 'secondary')
        status_display = dict(OrderState.CHOICES).get(obj.status, obj.status)
        return format_html('<span class="badge bg-{}">{}</span>', color, status_display)
    status_badge.short_description = _('Status')
    status_badge.admin_order_field = 'status'
    
    def assigned_courier_display(self, obj):
        if obj.assigned_courier:
            return format_html('<span class="courier-tag">{}</span>', obj.assigned_courier.get_full_name() or obj.assigned_courier.username)
        return format_html('<span class="unassigned-tag">-</span>')
    assigned_courier_display.short_description = _('Courier')
    assigned_courier_display.admin_order_field = 'assigned_courier'
    
    def pickup_city(self, obj):
        try:
            return obj.pickup_address.city
        except PickupAddress.DoesNotExist:
            return '-'
    pickup_city.short_description = _('Pickup City')
    
    def dropoff_city(self, obj):
        try:
            return obj.dropoff_address.city
        except DropoffAddress.DoesNotExist:
            return '-'
    dropoff_city.short_description = _('Dropoff City')
    
    def two_man_delivery_icon(self, obj):
        if obj.two_man_delivery:
            return format_html('<span class="two-man-icon">👥</span>')
        return ''
    two_man_delivery_icon.short_description = ''
    
    def mark_as_accepted(self, request, queryset):
        updated = queryset.update(status=OrderState.ACCEPTED, updated_by=request.user)
        self.message_user(request, _(f"{updated} orders marked as accepted."))
    mark_as_accepted.short_description = _("Mark selected orders as accepted")
    
    def mark_as_shipped(self, request, queryset):
        updated = queryset.update(status=OrderState.SHIPPED, updated_by=request.user)
        self.message_user(request, _(f"{updated} orders marked as shipped."))
    mark_as_shipped.short_description = _("Mark selected orders as shipped")
    
    def mark_as_delivered(self, request, queryset):
        updated = queryset.update(status=OrderState.DELIVERED, updated_by=request.user)
        self.message_user(request, _(f"{updated} orders marked as delivered."))
    mark_as_delivered.short_description = _("Mark selected orders as delivered")
    
    def mark_as_canceled(self, request, queryset):
        updated = queryset.update(status=OrderState.CANCELED, updated_by=request.user)
        self.message_user(request, _(f"{updated} orders marked as canceled."))
    mark_as_canceled.short_description = _("Mark selected orders as canceled")
    
    def export_as_csv(self, request, queryset):
        meta = self.model._meta
        field_names = [field.name for field in meta.fields]
        
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename={meta.verbose_name_plural.lower()}-{datetime.now().strftime("%Y%m%d")}.csv'
        writer = csv.writer(response)
        
        # Write header row
        writer.writerow(field_names)
        
        # Write data rows
        for obj in queryset:
            writer.writerow([getattr(obj, field) for field in field_names])
            
        return response
    export_as_csv.short_description = _("Export selected orders as CSV")
    
    def save_model(self, request, obj, form, change):
        """Set the created_by and updated_by fields when saved from admin"""
        if not change:  # New object
            obj.created_by = request.user
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)
    
    def save_formset(self, request, form, formset, change):
        """Set the created_by and updated_by fields for inline objects"""
        instances = formset.save(commit=False)
        
        for instance in instances:
            if not instance.pk:  # New object
                instance.created_by = request.user
            instance.updated_by = request.user
            instance.save()
        
        # Also handle deleted objects
        for obj in formset.deleted_objects:
            obj.delete()
        
        formset.save_m2m()
