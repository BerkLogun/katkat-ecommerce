from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.db import connection
from .models import Tenant, TenantStorefront, Product, Order, OrderItem
from .api_management import validate_api_key_from_request, add_cors_headers
import json
from decimal import Decimal
import uuid

def get_tenant_from_request(request):
    """Extract tenant from request headers or fallback to origin"""
    # Priority 1: Check for API key validation (most secure)
    tenant = validate_api_key_from_request(request)
    if tenant:
        return tenant.schema_name
    
    # Priority 2: Check for X-Tenant-ID header
    tenant_id = request.META.get('HTTP_X_TENANT_ID')
    if tenant_id:
        tenant = tenant_id.lower().replace(' ', '_')
    else:
        # Priority 3: Fallback to origin header
        origin = request.META.get('HTTP_ORIGIN', '')
        if origin and 'localhost' in origin:
            origin_host = origin.replace('http://', '').replace('https://', '').split(':')[0]
            if '.' in origin_host and origin_host != 'localhost':
                tenant = origin_host.split('.')[0]
            else:
                tenant = 'default_schema'
        else:
            tenant = 'default_schema'
    
    # Map 'default' to 'default_schema' for consistency
    if tenant == 'default':
        tenant = 'default_schema'
    
    return tenant

def set_tenant_schema(tenant):
    """Set the database search path for the given tenant"""
    with connection.cursor() as cursor:
        cursor.execute(f'SET search_path TO "{tenant}", public;')

@csrf_exempt
def get_storefront_config(request):
    if request.method == "OPTIONS":
        return add_cors_headers(JsonResponse({}), request)
    if request.method != "GET":
        return add_cors_headers(JsonResponse({"error": "Method not allowed"}, status=405), request)
    """Get tenant storefront configuration"""
    try:
        tenant_schema = get_tenant_from_request(request)
        set_tenant_schema(tenant_schema)
        
        # Get tenant info
        try:
            tenant = Tenant.objects.get(schema_name=tenant_schema)
        except Tenant.DoesNotExist:
            return add_cors_headers(JsonResponse({
                "error": "Tenant not found"
            }, status=404), request)
        
        # Get or create storefront config
        storefront, created = TenantStorefront.objects.get_or_create(
            tenant=tenant,
            defaults={
                'store_name': f"{tenant.name} Store",
                'primary_color': '#667eea',
                'secondary_color': '#764ba2',
                'accent_color': '#e74c3c',
                'background_color': '#f8f9fa',
                'text_color': '#333333'
            }
        )
        
        config = {
            'tenant': {
                'id': str(tenant.id),
                'name': tenant.name,
                'schema_name': tenant.schema_name,
                'domain': tenant.domain
            },
            'storefront': {
                'id': str(storefront.id),
                'store_name': storefront.store_name,
                'store_description': storefront.store_description,
                'store_logo_url': storefront.store_logo_url,
                'store_favicon_url': storefront.store_favicon_url,
                'theme_config': storefront.get_theme_config(),
                'custom_css': storefront.custom_css,
                'custom_js': storefront.custom_js,
                'seo': {
                    'meta_title': storefront.meta_title,
                    'meta_description': storefront.meta_description,
                    'meta_keywords': storefront.meta_keywords
                },
                'social_media': {
                    'facebook': storefront.facebook_url,
                    'twitter': storefront.twitter_url,
                    'instagram': storefront.instagram_url,
                    'linkedin': storefront.linkedin_url
                },
                'contact': {
                    'email': storefront.contact_email,
                    'phone': storefront.contact_phone,
                    'address': storefront.contact_address
                },
                'analytics': {
                    'google_analytics': storefront.google_analytics_id,
                    'facebook_pixel': storefront.facebook_pixel_id
                }
            }
        }
        
        return add_cors_headers(JsonResponse(config), request)
        
    except Exception as e:
        return add_cors_headers(JsonResponse({
            "error": str(e)
        }, status=500), request)

@csrf_exempt
def update_storefront_config(request):
    if request.method == "OPTIONS":
        return add_cors_headers(JsonResponse({}), request)
    if request.method != "PUT":
        return add_cors_headers(JsonResponse({"error": "Method not allowed"}, status=405), request)
    """Update tenant storefront configuration"""
    try:
        tenant_schema = get_tenant_from_request(request)
        set_tenant_schema(tenant_schema)
        
        data = json.loads(request.body)
        
        # Get tenant
        try:
            tenant = Tenant.objects.get(schema_name=tenant_schema)
        except Tenant.DoesNotExist:
            return add_cors_headers(JsonResponse({
                "error": "Tenant not found"
            }, status=404), request)
        
        # Get or create storefront
        storefront, created = TenantStorefront.objects.get_or_create(tenant=tenant)
        
        # Update store information
        if 'store_name' in data:
            storefront.store_name = data['store_name']
        if 'store_description' in data:
            storefront.store_description = data['store_description']
        if 'store_logo_url' in data:
            storefront.store_logo_url = data['store_logo_url']
        if 'store_favicon_url' in data:
            storefront.store_favicon_url = data['store_favicon_url']
        
        # Update theme colors
        if 'colors' in data:
            colors = data['colors']
            if 'primary' in colors:
                storefront.primary_color = colors['primary']
            if 'secondary' in colors:
                storefront.secondary_color = colors['secondary']
            if 'accent' in colors:
                storefront.accent_color = colors['accent']
            if 'background' in colors:
                storefront.background_color = colors['background']
            if 'text' in colors:
                storefront.text_color = colors['text']
        
        # Update layout settings
        if 'layout' in data:
            layout = data['layout']
            if 'type' in layout:
                storefront.layout_type = layout['type']
            if 'products_per_page' in layout:
                storefront.products_per_page = layout['products_per_page']
            if 'show_images' in layout:
                storefront.show_product_images = layout['show_images']
            if 'show_prices' in layout:
                storefront.show_product_prices = layout['show_prices']
            if 'show_descriptions' in layout:
                storefront.show_product_descriptions = layout['show_descriptions']
        
        # Update features
        if 'features' in data:
            features = data['features']
            if 'search' in features:
                storefront.enable_search = features['search']
            if 'filters' in features:
                storefront.enable_filters = features['filters']
            if 'sorting' in features:
                storefront.enable_sorting = features['sorting']
            if 'wishlist' in features:
                storefront.enable_wishlist = features['wishlist']
            if 'reviews' in features:
                storefront.enable_reviews = features['reviews']
            if 'related_products' in features:
                storefront.enable_related_products = features['related_products']
        
        # Update checkout settings
        if 'checkout' in data:
            checkout = data['checkout']
            if 'guest_checkout' in checkout:
                storefront.enable_guest_checkout = checkout['guest_checkout']
            if 'require_account' in checkout:
                storefront.require_account_creation = checkout['require_account']
            if 'coupons' in checkout:
                storefront.enable_coupons = checkout['coupons']
            if 'gift_cards' in checkout:
                storefront.enable_gift_cards = checkout['gift_cards']
        
        # Update custom CSS/JS
        if 'custom_css' in data:
            storefront.custom_css = data['custom_css']
        if 'custom_js' in data:
            storefront.custom_js = data['custom_js']
        
        # Update SEO
        if 'seo' in data:
            seo = data['seo']
            if 'meta_title' in seo:
                storefront.meta_title = seo['meta_title']
            if 'meta_description' in seo:
                storefront.meta_description = seo['meta_description']
            if 'meta_keywords' in seo:
                storefront.meta_keywords = seo['meta_keywords']
        
        # Update social media
        if 'social_media' in data:
            social = data['social_media']
            if 'facebook' in social:
                storefront.facebook_url = social['facebook']
            if 'twitter' in social:
                storefront.twitter_url = social['twitter']
            if 'instagram' in social:
                storefront.instagram_url = social['instagram']
            if 'linkedin' in social:
                storefront.linkedin_url = social['linkedin']
        
        # Update contact info
        if 'contact' in data:
            contact = data['contact']
            if 'email' in contact:
                storefront.contact_email = contact['email']
            if 'phone' in contact:
                storefront.contact_phone = contact['phone']
            if 'address' in contact:
                storefront.contact_address = contact['address']
        
        # Update analytics
        if 'analytics' in data:
            analytics = data['analytics']
            if 'google_analytics' in analytics:
                storefront.google_analytics_id = analytics['google_analytics']
            if 'facebook_pixel' in analytics:
                storefront.facebook_pixel_id = analytics['facebook_pixel']
        
        storefront.save()
        
        return add_cors_headers(JsonResponse({
            "success": True,
            "message": "Storefront configuration updated successfully",
            "storefront_id": str(storefront.id)
        }), request)
        
    except Exception as e:
        return add_cors_headers(JsonResponse({
            "error": str(e)
        }, status=500), request)

@csrf_exempt
def get_products_for_storefront(request):
    if request.method == "OPTIONS":
        return add_cors_headers(JsonResponse({}), request)
    if request.method != "GET":
        return add_cors_headers(JsonResponse({"error": "Method not allowed"}, status=405), request)
    """Get products for storefront with tenant-specific configuration"""
    try:
        tenant_schema = get_tenant_from_request(request)
        set_tenant_schema(tenant_schema)
        
        # Get storefront config
        try:
            tenant = Tenant.objects.get(schema_name=tenant_schema)
            storefront = TenantStorefront.objects.get(tenant=tenant)
        except (Tenant.DoesNotExist, TenantStorefront.DoesNotExist):
            return add_cors_headers(JsonResponse({
                "error": "Storefront configuration not found"
            }, status=404), request)
        
        # Get products with pagination
        page = int(request.GET.get('page', 1))
        per_page = storefront.products_per_page
        offset = (page - 1) * per_page
        
        products = Product.objects.filter(is_active=True)[offset:offset + per_page]
        
        products_data = []
        for product in products:
            product_data = {
                'id': str(product.id),
                'name': product.name,
                'price': float(product.price),
                'stock': product.stock,
                'created_at': product.created_at.isoformat(),
            }
            
            # Add optional fields based on storefront settings
            if storefront.show_product_descriptions:
                product_data['description'] = product.description
            if storefront.show_product_images and product.image_url:
                product_data['image_url'] = product.image_url
            
            products_data.append(product_data)
        
        # Get total count for pagination
        total_products = Product.objects.filter(is_active=True).count()
        total_pages = (total_products + per_page - 1) // per_page
        
        response_data = {
            'products': products_data,
            'pagination': {
                'current_page': page,
                'total_pages': total_pages,
                'total_products': total_products,
                'per_page': per_page
            },
            'storefront_config': {
                'layout_type': storefront.layout_type,
                'show_images': storefront.show_product_images,
                'show_prices': storefront.show_product_prices,
                'show_descriptions': storefront.show_product_descriptions,
                'enable_search': storefront.enable_search,
                'enable_filters': storefront.enable_filters,
                'enable_sorting': storefront.enable_sorting
            }
        }
        
        return add_cors_headers(JsonResponse(response_data), request)
        
    except Exception as e:
        return add_cors_headers(JsonResponse({
            "error": str(e)
        }, status=500), request)

@csrf_exempt
def create_order_for_storefront(request):
    if request.method == "OPTIONS":
        return add_cors_headers(JsonResponse({}), request)
    if request.method != "POST":
        return add_cors_headers(JsonResponse({"error": "Method not allowed"}, status=405), request)
    """Create order for storefront with tenant-specific checkout settings"""
    try:
        tenant_schema = get_tenant_from_request(request)
        set_tenant_schema(tenant_schema)
        
        # Get storefront config
        try:
            tenant = Tenant.objects.get(schema_name=tenant_schema)
            storefront = TenantStorefront.objects.get(tenant=tenant)
        except (Tenant.DoesNotExist, TenantStorefront.DoesNotExist):
            return add_cors_headers(JsonResponse({
                "error": "Storefront configuration not found"
            }, status=404), request)
        
        data = json.loads(request.body)
        
        # Check if guest checkout is enabled
        if not storefront.enable_guest_checkout and not data.get('customer_account_id'):
            return add_cors_headers(JsonResponse({
                "error": "Guest checkout is disabled for this store"
            }, status=400), request)
        
        # Generate order number
        order_number = f"ORD-{uuid.uuid4().hex[:8].upper()}"
        
        # Create order
        order = Order.objects.create(
            order_number=order_number,
            customer_name=data['customer_name'],
            customer_email=data['customer_email'],
            total_amount=Decimal(data['total_amount']),
        )
        
        # Create order items
        for item_data in data['items']:
            product = Product.objects.get(id=item_data['product_id'])
            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=item_data['quantity'],
                price=Decimal(item_data['price']),
            )
            # Update stock
            product.stock -= item_data['quantity']
            product.save()
        
        return add_cors_headers(JsonResponse({
            'success': True,
            'order': {
                'id': str(order.id),
                'order_number': order.order_number,
                'total_amount': float(order.total_amount),
                'customer_name': order.customer_name,
                'customer_email': order.customer_email
            }
        }), request)
        
    except Exception as e:
        return add_cors_headers(JsonResponse({
            "error": str(e)
        }, status=500), request) 