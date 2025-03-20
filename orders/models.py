from django.db import models
from django.utils.translation import gettext_lazy as _
from accounts.models import User, CustomerProfile
from core.models import AuditableMixin

class WeightClass(models.TextChoices):
    LIGHT = "LIGHT", _("Light (0-5kg)")
    MEDIUM = "MEDIUM", _("Medium (5-20kg)")
    HEAVY = "HEAVY", _("Heavy (20-50kg)")
    VERY_HEAVY = "VERY_HEAVY", _("Very Heavy (50kg+)")

class OrderState:
    NEW = "new"
    CANCELED = "canceled"
    EXPIRED = "expired"
    ACCEPTED = "accepted"
    SHIPPED = "shipped"
    DISPUTED = "disputed"
    COMPLETED = "completed"
    DELIVERED = "delivered"

    CHOICES = [
        (NEW, _("New")),
        (CANCELED, _("Canceled")),
        (ACCEPTED, _("Accepted")),
        (SHIPPED, _("Shipped")),
        (DISPUTED, _("Disputed")),
        (COMPLETED, _("Completed")),
        (EXPIRED, _("Expired")),
        (DELIVERED, _("Delivered")),
    ]

class Order(models.Model):
    """
    Model to store order information from Whoppah
    """
    # Order Information
    order_date = models.DateTimeField(_("Order Date"))
    order_id = models.CharField(_("Order ID"), max_length=50, unique=True)
    order_url = models.URLField(_("Order URL"), max_length=255, blank=True)
    
    # Product Information
    product_url = models.URLField(_("Product URL"), max_length=255, blank=True)
    product_category = models.CharField(_("Product Category"), max_length=100, blank=True)
    product_name = models.CharField(_("Product Name"), max_length=255)
    weight = models.DecimalField(
        _("weight"),
        blank=True,
        null=True,
        max_digits=12,
        decimal_places=2,
    )
    two_man_delivery = models.BooleanField(_("2-Man Delivery Required"), default=False)
    
    # Product Dimensions
    height = models.PositiveIntegerField(_("Height (cm)"), null=True, blank=True)
    width = models.PositiveIntegerField(_("Width (cm)"), null=True, blank=True)
    depth = models.PositiveIntegerField(_("Depth (cm)"), null=True, blank=True)
    seat_height = models.PositiveIntegerField(_("Seat Height (cm)"), null=True, blank=True)
    
    # Delivery Information
    number_of_parcels = models.PositiveIntegerField(_("Number of Parcels"), default=1)
    
    # Price Information
    total_price = models.DecimalField(_("Total incl VAT"), max_digits=10, decimal_places=2)
    
    # Order Status
    status = models.CharField(
        _("Order Status"),
        max_length=20,
        choices=OrderState.CHOICES,
        default=OrderState.NEW
    )
    
    # Courier Assignment
    assigned_courier = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="assigned_orders",
        limit_choices_to={"user_type": User.Types.COURIER}
    )
    
    # Audit Fields
    created_by = models.ForeignKey(
        User,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="%(app_label)s_%(class)s_created",
        verbose_name=_('Created By')
    )
    updated_by = models.ForeignKey(
        User,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="%(app_label)s_%(class)s_updated",
        verbose_name=_('Updated By')
    )
    created_at = models.DateTimeField(_('Created At'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Updated At'), auto_now=True)
    
    def __str__(self):
        return f"Order #{self.order_id} - {self.product_name}"
    
    class Meta:
        ordering = ['-order_date']
        verbose_name = _("Order")
        verbose_name_plural = _("Orders")
    
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

class PickupAddress(models.Model):
    """
    Model to store pickup address information for orders
    """
    order = models.OneToOneField(
        Order,
        on_delete=models.CASCADE,
        related_name="pickup_address"
    )
    customer_name = models.CharField(_("Customer Name"), max_length=255)
    address = models.TextField(_("Address"))
    postal_code = models.CharField(_("Postal Code"), max_length=20)
    city = models.CharField(_("City"), max_length=100)
    country = models.CharField(_("Country"), max_length=100)
    email = models.EmailField(_("Email"))
    phone_number = models.CharField(_("Phone Number"), max_length=20)
    
    # Audit Fields
    created_by = models.ForeignKey(
        User,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="%(app_label)s_%(class)s_created",
        verbose_name=_('Created By')
    )
    updated_by = models.ForeignKey(
        User,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="%(app_label)s_%(class)s_updated",
        verbose_name=_('Updated By')
    )
    created_at = models.DateTimeField(_('Created At'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Updated At'), auto_now=True)
    
    def __str__(self):
        return f"Pickup: {self.customer_name}, {self.city}"
    
    class Meta:
        verbose_name = _("Pickup Address")
        verbose_name_plural = _("Pickup Addresses")
    
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

class DropoffAddress(models.Model):
    """
    Model to store dropoff address information for orders
    """
    order = models.OneToOneField(
        Order,
        on_delete=models.CASCADE,
        related_name="dropoff_address"
    )
    customer_name = models.CharField(_("Customer Name"), max_length=255)
    address = models.TextField(_("Address"))
    postal_code = models.CharField(_("Postal Code"), max_length=20)
    city = models.CharField(_("City"), max_length=100)
    country = models.CharField(_("Country"), max_length=100)
    email = models.EmailField(_("Email"))
    phone_number = models.CharField(_("Phone Number"), max_length=20)
    
    # Audit Fields
    created_by = models.ForeignKey(
        User,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="%(app_label)s_%(class)s_created",
        verbose_name=_('Created By')
    )
    updated_by = models.ForeignKey(
        User,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="%(app_label)s_%(class)s_updated",
        verbose_name=_('Updated By')
    )
    created_at = models.DateTimeField(_('Created At'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Updated At'), auto_now=True)
    
    def __str__(self):
        return f"Dropoff: {self.customer_name}, {self.city}"
    
    class Meta:
        verbose_name = _("Dropoff Address")
        verbose_name_plural = _("Dropoff Addresses")
    
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

class OrderNote(models.Model):
    """
    Model to store notes related to orders
    """
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="notes"
    )
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name="order_notes"
    )
    content = models.TextField(_("Note Content"))
    created_at = models.DateTimeField(auto_now_add=True)
    
    # Additional Audit Fields
    updated_by = models.ForeignKey(
        User,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="%(app_label)s_%(class)s_updated",
        verbose_name=_('Updated By')
    )
    updated_at = models.DateTimeField(_('Updated At'), auto_now=True)
    
    def __str__(self):
        return f"Note for Order #{self.order.order_id}"
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = _("Order Note")
        verbose_name_plural = _("Order Notes")
    
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
