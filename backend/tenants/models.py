import uuid
import hashlib
import secrets
from datetime import datetime, timedelta
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.utils import timezone


class Tenant(models.Model):
    """Enhanced tenant model for multi-tenancy"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, unique=True)
    schema_name = models.CharField(max_length=63, unique=True, validators=[
        RegexValidator(
            regex='^[a-z][a-z0-9_]*$',
            message='Schema name must start with a letter and contain only lowercase letters, numbers, and underscores.'
        )
    ])
    domain = models.CharField(max_length=200, blank=True, null=True)
    subdomain = models.CharField(max_length=100, blank=True, null=True)
    owner = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='tenants', null=True, blank=True)
    
    # Tenant status
    is_active = models.BooleanField(default=True)
    is_verified = models.BooleanField(default=False)
    is_premium = models.BooleanField(default=False)
    
    # Billing and limits
    plan_type = models.CharField(max_length=20, choices=[
        ('free', 'Free'),
        ('basic', 'Basic'),
        ('pro', 'Professional'),
        ('enterprise', 'Enterprise'),
    ], default='free')
    
    product_limit = models.IntegerField(default=100)
    order_limit = models.IntegerField(default=1000)
    storage_limit_mb = models.IntegerField(default=100)
    
    # Contact information
    contact_email = models.EmailField(blank=True)
    contact_phone = models.CharField(max_length=20, blank=True)
    contact_address = models.TextField(blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    trial_ends_at = models.DateTimeField(null=True, blank=True)
    subscription_ends_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        db_table = 'tenants'
        ordering = ['-created_at']
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.schema_name:
            self.schema_name = self.name.lower().replace(' ', '_').replace('-', '_')
        super().save(*args, **kwargs)
    
    @property
    def is_trial_active(self):
        if not self.trial_ends_at:
            return False
        return self.trial_ends_at > timezone.now()
    
    @property
    def is_subscription_active(self):
        if not self.subscription_ends_at:
            return True
        return self.subscription_ends_at > timezone.now()
    
    def get_usage_stats(self):
        """Get current usage statistics"""
        from products.models import Product
        from orders.models import Order
        
        return {
            'products_count': Product.objects.count(),
            'orders_count': Order.objects.count(),
            'storage_used_mb': self.get_storage_usage(),
        }
    
    def get_storage_usage(self):
        """Calculate storage usage in MB"""
        # This would be implemented based on your file storage system
        return 0


class Domain(models.Model):
    """Domain model for tenant routing"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name='domains')
    domain = models.CharField(max_length=253, unique=True)
    is_primary = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'tenant_domains'
    
    def __str__(self):
        return self.domain


class ApiKey(models.Model):
    """Enhanced API Key model for secure tenant authentication"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name='api_keys')
    name = models.CharField(max_length=100)
    key_hash = models.CharField(max_length=255, unique=True)
    key_prefix = models.CharField(max_length=8)
    
    # Permissions
    permissions = models.JSONField(default=list)
    is_active = models.BooleanField(default=True)
    
    # Usage tracking
    expires_at = models.DateTimeField(null=True, blank=True)
    last_used_at = models.DateTimeField(null=True, blank=True)
    usage_count = models.IntegerField(default=0)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'api_keys'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.tenant.name} - {self.name}"
    
    @classmethod
    def generate_key(cls):
        """Generate a new API key"""
        return f"katkat_{secrets.token_urlsafe(32)}"
    
    @classmethod
    def hash_key(cls, key):
        """Hash an API key for storage"""
        return hashlib.sha256(key.encode()).hexdigest()
    
    @classmethod
    def validate_key(cls, key):
        """Validate an API key and return the associated tenant"""
        if not key or not key.startswith('katkat_'):
            return None
        
        key_hash = cls.hash_key(key)
        try:
            api_key = cls.objects.select_related('tenant').get(
                key_hash=key_hash,
                is_active=True
            )
            
            if api_key.expires_at and api_key.expires_at < timezone.now():
                return None
            
            # Update usage statistics
            api_key.last_used_at = timezone.now()
            api_key.usage_count += 1
            api_key.save(update_fields=['last_used_at', 'usage_count'])
            
            return api_key.tenant
        except cls.DoesNotExist:
            return None


class TenantSettings(models.Model):
    """Tenant-specific settings and configuration"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    tenant = models.OneToOneField(Tenant, on_delete=models.CASCADE, related_name='settings')
    
    # General settings
    timezone = models.CharField(max_length=50, default='UTC')
    currency = models.CharField(max_length=3, default='USD')
    language = models.CharField(max_length=10, default='en')
    
    # Email settings
    email_from_name = models.CharField(max_length=100, blank=True)
    email_from_address = models.EmailField(blank=True)
    email_signature = models.TextField(blank=True)
    
    # Notification settings
    email_notifications = models.BooleanField(default=True)
    sms_notifications = models.BooleanField(default=False)
    push_notifications = models.BooleanField(default=False)
    
    # Security settings
    require_2fa = models.BooleanField(default=False)
    session_timeout_minutes = models.IntegerField(default=480)  # 8 hours
    max_login_attempts = models.IntegerField(default=5)
    
    # Integration settings
    google_analytics_id = models.CharField(max_length=50, blank=True)
    facebook_pixel_id = models.CharField(max_length=50, blank=True)
    stripe_public_key = models.CharField(max_length=100, blank=True)
    stripe_secret_key = models.CharField(max_length=100, blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'tenant_settings'
    
    def __str__(self):
        return f"{self.tenant.name} Settings" 