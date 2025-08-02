import uuid
import json
from django.db import models
from django.core.validators import URLValidator
from django.utils import timezone
from tenants.models import Tenant


class Storefront(models.Model):
    """Enhanced storefront model with comprehensive customization options"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    tenant = models.OneToOneField(Tenant, on_delete=models.CASCADE, related_name='storefront')
    
    # Basic Information
    store_name = models.CharField(max_length=200, default='My Store')
    store_description = models.TextField(blank=True)
    store_tagline = models.CharField(max_length=200, blank=True)
    
    # Branding
    logo_url = models.URLField(blank=True, validators=[URLValidator()])
    favicon_url = models.URLField(blank=True, validators=[URLValidator()])
    hero_image_url = models.URLField(blank=True, validators=[URLValidator()])
    
    # Contact Information
    contact_email = models.EmailField(blank=True)
    contact_phone = models.CharField(max_length=20, blank=True)
    contact_address = models.TextField(blank=True)
    business_hours = models.JSONField(default=dict, blank=True)
    
    # Social Media
    social_links = models.JSONField(default=dict, blank=True)
    
    # SEO Settings
    meta_title = models.CharField(max_length=60, blank=True)
    meta_description = models.TextField(blank=True)
    meta_keywords = models.CharField(max_length=255, blank=True)
    og_image_url = models.URLField(blank=True, validators=[URLValidator()])
    
    # Analytics
    google_analytics_id = models.CharField(max_length=50, blank=True)
    facebook_pixel_id = models.CharField(max_length=50, blank=True)
    google_tag_manager_id = models.CharField(max_length=50, blank=True)
    
    # Status
    is_active = models.BooleanField(default=True)
    is_published = models.BooleanField(default=False)
    published_at = models.DateTimeField(null=True, blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'storefronts'
    
    def __str__(self):
        return f"{self.tenant.name} Storefront"
    
    def publish(self):
        """Publish the storefront"""
        self.is_published = True
        self.published_at = timezone.now()
        self.save()
    
    def unpublish(self):
        """Unpublish the storefront"""
        self.is_published = False
        self.published_at = None
        self.save()


class Theme(models.Model):
    """Theme configuration for storefronts"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    storefront = models.OneToOneField(Storefront, on_delete=models.CASCADE, related_name='theme')
    
    # Color Scheme
    primary_color = models.CharField(max_length=7, default='#667eea')
    secondary_color = models.CharField(max_length=7, default='#764ba2')
    accent_color = models.CharField(max_length=7, default='#e74c3c')
    background_color = models.CharField(max_length=7, default='#f8f9fa')
    text_color = models.CharField(max_length=7, default='#333333')
    link_color = models.CharField(max_length=7, default='#007bff')
    success_color = models.CharField(max_length=7, default='#28a745')
    warning_color = models.CharField(max_length=7, default='#ffc107')
    error_color = models.CharField(max_length=7, default='#dc3545')
    
    # Typography
    font_family = models.CharField(max_length=100, default='Inter, sans-serif')
    heading_font_family = models.CharField(max_length=100, default='Inter, sans-serif')
    font_size_base = models.CharField(max_length=10, default='16px')
    line_height_base = models.DecimalField(max_digits=3, decimal_places=2, default=1.5)
    
    # Layout
    layout_type = models.CharField(max_length=20, choices=[
        ('grid', 'Grid Layout'),
        ('list', 'List Layout'),
        ('masonry', 'Masonry Layout'),
        ('carousel', 'Carousel Layout'),
    ], default='grid')
    
    container_width = models.CharField(max_length=20, default='1200px')
    sidebar_position = models.CharField(max_length=10, choices=[
        ('left', 'Left'),
        ('right', 'Right'),
        ('none', 'None'),
    ], default='left')
    
    # Spacing
    spacing_unit = models.CharField(max_length=10, default='1rem')
    border_radius = models.CharField(max_length=10, default='0.375rem')
    box_shadow = models.CharField(max_length=100, default='0 2px 4px rgba(0,0,0,0.1)')
    
    # Custom CSS/JS
    custom_css = models.TextField(blank=True)
    custom_js = models.TextField(blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'storefront_themes'
    
    def __str__(self):
        return f"{self.storefront.tenant.name} Theme"
    
    def get_css_variables(self):
        """Get CSS custom properties for the theme"""
        return {
            '--primary-color': self.primary_color,
            '--secondary-color': self.secondary_color,
            '--accent-color': self.accent_color,
            '--background-color': self.background_color,
            '--text-color': self.text_color,
            '--link-color': self.link_color,
            '--success-color': self.success_color,
            '--warning-color': self.warning_color,
            '--error-color': self.error_color,
            '--font-family': self.font_family,
            '--heading-font-family': self.heading_font_family,
            '--font-size-base': self.font_size_base,
            '--line-height-base': str(self.line_height_base),
            '--spacing-unit': self.spacing_unit,
            '--border-radius': self.border_radius,
            '--box-shadow': self.box_shadow,
        }


class StorefrontSettings(models.Model):
    """Storefront-specific settings and features"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    storefront = models.OneToOneField(Storefront, on_delete=models.CASCADE, related_name='settings')
    
    # Product Display
    products_per_page = models.IntegerField(default=12)
    show_product_images = models.BooleanField(default=True)
    show_product_prices = models.BooleanField(default=True)
    show_product_descriptions = models.BooleanField(default=True)
    show_product_ratings = models.BooleanField(default=True)
    show_product_stock = models.BooleanField(default=True)
    
    # Features
    enable_search = models.BooleanField(default=True)
    enable_filters = models.BooleanField(default=True)
    enable_sorting = models.BooleanField(default=True)
    enable_wishlist = models.BooleanField(default=False)
    enable_reviews = models.BooleanField(default=False)
    enable_related_products = models.BooleanField(default=True)
    enable_quick_view = models.BooleanField(default=True)
    enable_compare_products = models.BooleanField(default=False)
    
    # Checkout Settings
    enable_guest_checkout = models.BooleanField(default=True)
    require_account_creation = models.BooleanField(default=False)
    enable_coupons = models.BooleanField(default=False)
    enable_gift_cards = models.BooleanField(default=False)
    enable_tax_calculation = models.BooleanField(default=True)
    enable_shipping_calculation = models.BooleanField(default=True)
    
    # Payment Methods
    payment_methods = models.JSONField(default=list, blank=True)
    
    # Shipping
    shipping_methods = models.JSONField(default=list, blank=True)
    free_shipping_threshold = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    
    # Email Notifications
    order_confirmation_email = models.BooleanField(default=True)
    shipping_confirmation_email = models.BooleanField(default=True)
    abandoned_cart_email = models.BooleanField(default=False)
    
    # Security
    require_ssl = models.BooleanField(default=True)
    enable_captcha = models.BooleanField(default=False)
    max_login_attempts = models.IntegerField(default=5)
    
    # Performance
    enable_caching = models.BooleanField(default=True)
    enable_cdn = models.BooleanField(default=False)
    image_optimization = models.BooleanField(default=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'storefront_settings'
    
    def __str__(self):
        return f"{self.storefront.tenant.name} Settings"


class Page(models.Model):
    """Custom pages for storefronts"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    storefront = models.ForeignKey(Storefront, on_delete=models.CASCADE, related_name='pages')
    
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    content = models.TextField()
    meta_title = models.CharField(max_length=60, blank=True)
    meta_description = models.TextField(blank=True)
    
    # Page settings
    is_active = models.BooleanField(default=True)
    is_published = models.BooleanField(default=False)
    show_in_navigation = models.BooleanField(default=False)
    navigation_order = models.IntegerField(default=0)
    
    # SEO
    canonical_url = models.URLField(blank=True)
    robots_index = models.BooleanField(default=True)
    robots_follow = models.BooleanField(default=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        db_table = 'storefront_pages'
        ordering = ['navigation_order', 'title']
        unique_together = ['storefront', 'slug']
    
    def __str__(self):
        return f"{self.storefront.tenant.name} - {self.title}"
    
    def publish(self):
        """Publish the page"""
        self.is_published = True
        self.published_at = timezone.now()
        self.save()


class Navigation(models.Model):
    """Navigation menu configuration"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    storefront = models.ForeignKey(Storefront, on_delete=models.CASCADE, related_name='navigations')
    
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=20, choices=[
        ('header', 'Header'),
        ('footer', 'Footer'),
        ('sidebar', 'Sidebar'),
        ('mobile', 'Mobile'),
    ])
    
    # Menu structure as JSON
    menu_items = models.JSONField(default=list, blank=True)
    
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'storefront_navigations'
        unique_together = ['storefront', 'location']
    
    def __str__(self):
        return f"{self.storefront.tenant.name} - {self.name} ({self.location})" 