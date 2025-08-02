from django.db import models
import uuid
import hashlib
import secrets
from datetime import datetime, timedelta
import json

class Tenant(models.Model):
    """Tenant model for managing multi-tenancy"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, unique=True)
    schema_name = models.CharField(max_length=100, unique=True)
    domain = models.CharField(max_length=200, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'tenants'
    
    def __str__(self):
        return self.name

class TenantStorefront(models.Model):
    """Tenant storefront customization settings"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    tenant = models.OneToOneField(Tenant, on_delete=models.CASCADE, related_name='storefront')
    
    # Store Information
    store_name = models.CharField(max_length=200, default='My Store')
    store_description = models.TextField(blank=True)
    store_logo_url = models.URLField(blank=True)
    store_favicon_url = models.URLField(blank=True)
    
    # Theme Settings
    primary_color = models.CharField(max_length=7, default='#667eea')  # Hex color
    secondary_color = models.CharField(max_length=7, default='#764ba2')
    accent_color = models.CharField(max_length=7, default='#e74c3c')
    background_color = models.CharField(max_length=7, default='#f8f9fa')
    text_color = models.CharField(max_length=7, default='#333333')
    
    # Layout Settings
    layout_type = models.CharField(max_length=20, choices=[
        ('grid', 'Grid Layout'),
        ('list', 'List Layout'),
        ('masonry', 'Masonry Layout')
    ], default='grid')
    
    products_per_page = models.IntegerField(default=12)
    show_product_images = models.BooleanField(default=True)
    show_product_prices = models.BooleanField(default=True)
    show_product_descriptions = models.BooleanField(default=True)
    
    # Features
    enable_search = models.BooleanField(default=True)
    enable_filters = models.BooleanField(default=True)
    enable_sorting = models.BooleanField(default=True)
    enable_wishlist = models.BooleanField(default=False)
    enable_reviews = models.BooleanField(default=False)
    enable_related_products = models.BooleanField(default=True)
    
    # Checkout Settings
    enable_guest_checkout = models.BooleanField(default=True)
    require_account_creation = models.BooleanField(default=False)
    enable_coupons = models.BooleanField(default=False)
    enable_gift_cards = models.BooleanField(default=False)
    
    # Custom CSS/JS
    custom_css = models.TextField(blank=True)
    custom_js = models.TextField(blank=True)
    
    # SEO Settings
    meta_title = models.CharField(max_length=60, blank=True)
    meta_description = models.TextField(blank=True)
    meta_keywords = models.CharField(max_length=255, blank=True)
    
    # Social Media
    facebook_url = models.URLField(blank=True)
    twitter_url = models.URLField(blank=True)
    instagram_url = models.URLField(blank=True)
    linkedin_url = models.URLField(blank=True)
    
    # Contact Information
    contact_email = models.EmailField(blank=True)
    contact_phone = models.CharField(max_length=20, blank=True)
    contact_address = models.TextField(blank=True)
    
    # Analytics
    google_analytics_id = models.CharField(max_length=50, blank=True)
    facebook_pixel_id = models.CharField(max_length=50, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'tenant_storefronts'
    
    def __str__(self):
        return f"{self.tenant.name} Storefront"
    
    def get_theme_config(self):
        """Get theme configuration as JSON"""
        return {
            'colors': {
                'primary': self.primary_color,
                'secondary': self.secondary_color,
                'accent': self.accent_color,
                'background': self.background_color,
                'text': self.text_color
            },
            'layout': {
                'type': self.layout_type,
                'products_per_page': self.products_per_page,
                'show_images': self.show_product_images,
                'show_prices': self.show_product_prices,
                'show_descriptions': self.show_product_descriptions
            },
            'features': {
                'search': self.enable_search,
                'filters': self.enable_filters,
                'sorting': self.enable_sorting,
                'wishlist': self.enable_wishlist,
                'reviews': self.enable_reviews,
                'related_products': self.enable_related_products
            },
            'checkout': {
                'guest_checkout': self.enable_guest_checkout,
                'require_account': self.require_account_creation,
                'coupons': self.enable_coupons,
                'gift_cards': self.enable_gift_cards
            }
        }

class ApiKey(models.Model):
    """API Key model for secure tenant authentication"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name='api_keys')
    name = models.CharField(max_length=100)  # Human-readable name for the key
    key_hash = models.CharField(max_length=255, unique=True)  # Hashed API key
    key_prefix = models.CharField(max_length=8)  # First 8 chars for identification
    is_active = models.BooleanField(default=True)
    expires_at = models.DateTimeField(null=True, blank=True)
    last_used_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'api_keys'
    
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
            
            # Check if key is expired
            if api_key.expires_at and api_key.expires_at < datetime.now():
                return None
            
            # Update last used timestamp
            api_key.last_used_at = datetime.now()
            api_key.save(update_fields=['last_used_at'])
            
            return api_key.tenant
        except cls.DoesNotExist:
            return None

class Product(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField(default=0)
    image_url = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        db_table = 'products'
    
    def __str__(self):
        return self.name

class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    order_number = models.CharField(max_length=20, unique=True)
    customer_email = models.EmailField()
    customer_name = models.CharField(max_length=200)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'orders'
    
    def __str__(self):
        return f"Order {self.order_number}"

class OrderItem(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    
    class Meta:
        db_table = 'order_items'
    
    def __str__(self):
        return f"{self.quantity}x {self.product.name}" 