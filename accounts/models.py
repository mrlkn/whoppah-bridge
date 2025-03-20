from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils.translation import gettext_lazy as _


class UserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError("The email must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular User with the given email and password."""
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("user_type", User.Types.ADMIN)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    """Custom User model with email as username field and additional fields for different roles."""

    class Types(models.TextChoices):
        ADMIN = "ADMIN", _("Admin")
        COURIER = "COURIER", _("Courier")
        CUSTOMER = "CUSTOMER", _("Customer")

    # Remove username field and use email instead
    username = None
    email = models.EmailField(_("email address"), unique=True)
    
    # Common fields for all user types
    user_type = models.CharField(
        _("User Type"), 
        max_length=10, 
        choices=Types.choices, 
        default=Types.CUSTOMER
    )
    phone_number = models.CharField(_("Phone Number"), max_length=15, blank=True)
    address = models.TextField(_("Address"), blank=True)
    
    # Fields for tracking creation and updates
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")

    def __str__(self):
        return self.email

    @property
    def is_admin(self):
        return self.user_type == self.Types.ADMIN
    
    @property
    def is_courier(self):
        return self.user_type == self.Types.COURIER
    
    @property
    def is_customer(self):
        return self.user_type == self.Types.CUSTOMER


class CourierProfile(models.Model):
    """Additional information for couriers."""
    
    user = models.OneToOneField(
        User, 
        on_delete=models.CASCADE, 
        related_name="courier_profile",
        limit_choices_to={"user_type": User.Types.COURIER}
    )
    vehicle_type = models.CharField(
        _("Vehicle Type"), 
        max_length=50,
        choices=[
            ("CAR", _("Car")),
            ("BIKE", _("Bike")),
            ("SCOOTER", _("Scooter")),
            ("VAN", _("Van")),
        ]
    )
    license_number = models.CharField(_("License Number"), max_length=50)
    availability_status = models.CharField(
        _("Availability Status"),
        max_length=20,
        choices=[
            ("AVAILABLE", _("Available")),
            ("BUSY", _("Busy")),
            ("OFFLINE", _("Offline")),
        ],
        default="OFFLINE"
    )
    max_delivery_distance = models.PositiveIntegerField(
        _("Maximum Delivery Distance (km)"),
        default=10
    )
    # Geographic area where the courier can deliver
    service_area = models.CharField(_("Service Area"), max_length=100, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Courier: {self.user.email}"


class CustomerProfile(models.Model):
    """Additional information for customers."""
    
    user = models.OneToOneField(
        User, 
        on_delete=models.CASCADE, 
        related_name="customer_profile",
        limit_choices_to={"user_type": User.Types.CUSTOMER}
    )
    default_shipping_address = models.TextField(_("Default Shipping Address"), blank=True)
    default_billing_address = models.TextField(_("Default Billing Address"), blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Customer: {self.user.email}"
