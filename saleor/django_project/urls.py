from django.contrib import admin
from django.urls import path
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.db import connection
from . import api
from . import api_management
from . import storefront_api

def health_check(request):
    response = JsonResponse({"status": "healthy", "service": "multi-tenant-demo"})
    response["Access-Control-Allow-Origin"] = "*"
    response["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
    response["Access-Control-Allow-Headers"] = "Content-Type, Authorization, X-Tenant-ID, X-API-Key"
    return response

def tenant_info(request):
    # Try to get tenant from host first
    host = request.get_host().split(":")[0]
    tenant = host.split(".")[0] if "." in host else "default"
    
    # If it's a cross-origin request, try to get tenant from Origin header
    origin = request.META.get('HTTP_ORIGIN', '')
    if origin and 'localhost' in origin:
        origin_host = origin.replace('http://', '').replace('https://', '').split(':')[0]
        if '.' in origin_host and origin_host != 'localhost':
            tenant = origin_host.split('.')[0]
    
    response = JsonResponse({
        "tenant": tenant,
        "host": host,
        "origin": origin,
        "message": f"Welcome to tenant: {tenant}"
    })
    response["Access-Control-Allow-Origin"] = "*"
    response["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
    response["Access-Control-Allow-Headers"] = "Content-Type, Authorization, X-Tenant-ID, X-API-Key"
    return response

@csrf_exempt
@require_http_methods(["OPTIONS"])
def cors_preflight(request):
    response = JsonResponse({})
    response["Access-Control-Allow-Origin"] = "*"
    response["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
    response["Access-Control-Allow-Headers"] = "Content-Type, Authorization, X-Tenant-ID, X-API-Key"
    return response

@csrf_exempt
def create_tenant(request):
    if request.method == 'POST':
        import json
        data = json.loads(request.body)
        tenant_name = data.get('name', '').lower().replace(' ', '_')
        
        if not tenant_name:
            return JsonResponse({"error": "Tenant name is required"}, status=400)
        
        try:
            with connection.cursor() as cursor:
                # Create schema for the tenant
                cursor.execute(f'CREATE SCHEMA IF NOT EXISTS "{tenant_name}";')
                
                # Set search path to the new schema
                cursor.execute(f'SET search_path TO "{tenant_name}", public;')
                
                # Run Django migrations for the tenant
                from django.core.management import execute_from_command_line
                execute_from_command_line(['manage.py', 'migrate', '--run-syncdb'])
                
            response = JsonResponse({
                "success": True,
                "tenant": tenant_name,
                "message": f"Tenant '{tenant_name}' created successfully with isolated database schema"
            })
            response["Access-Control-Allow-Origin"] = "*"
            return response
            
        except Exception as e:
            response = JsonResponse({
                "error": f"Failed to create tenant: {str(e)}"
            }, status=500)
            response["Access-Control-Allow-Origin"] = "*"
            return response
    
    response = JsonResponse({"error": "POST method required"}, status=405)
    response["Access-Control-Allow-Origin"] = "*"
    return response

@csrf_exempt
def initialize_tenant_data(request):
    if request.method == 'POST':
        import json
        data = json.loads(request.body)
        tenant_name = data.get('tenant', '').lower().replace(' ', '_')
        
        if not tenant_name:
            return JsonResponse({"error": "Tenant name is required"}, status=400)
        
        try:
            with connection.cursor() as cursor:
                # Create schema if it doesn't exist
                cursor.execute(f'CREATE SCHEMA IF NOT EXISTS "{tenant_name}";')
                
                # Set search path to the tenant schema
                cursor.execute(f'SET search_path TO "{tenant_name}", public;')
                
                # Run migrations for this tenant
                from django.core.management import execute_from_command_line
                execute_from_command_line(['manage.py', 'migrate', '--run-syncdb'])
                
                # Add sample products for this tenant
                from .models import Product
                from decimal import Decimal
                
                # Check if products already exist
                if Product.objects.count() == 0:
                    sample_products = [
                        {
                            'name': f'{tenant_name.title()} Laptop',
                            'description': f'High-performance laptop for {tenant_name} customers',
                            'price': Decimal('1299.99'),
                            'stock': 10,
                            'image_url': 'https://via.placeholder.com/300x200?text=Laptop'
                        },
                        {
                            'name': f'{tenant_name.title()} Headphones',
                            'description': f'Premium headphones for {tenant_name} customers',
                            'price': Decimal('299.99'),
                            'stock': 25,
                            'image_url': 'https://via.placeholder.com/300x200?text=Headphones'
                        },
                        {
                            'name': f'{tenant_name.title()} Smartphone',
                            'description': f'Latest smartphone for {tenant_name} customers',
                            'price': Decimal('899.99'),
                            'stock': 15,
                            'image_url': 'https://via.placeholder.com/300x200?text=Smartphone'
                        }
                    ]
                    
                    for product_data in sample_products:
                        Product.objects.create(**product_data)
                
            response = JsonResponse({
                "success": True,
                "tenant": tenant_name,
                "message": f"Tenant '{tenant_name}' initialized with sample data"
            })
            response["Access-Control-Allow-Origin"] = "*"
            return response
            
        except Exception as e:
            response = JsonResponse({
                "error": f"Failed to initialize tenant: {str(e)}"
            }, status=500)
            response["Access-Control-Allow-Origin"] = "*"
            return response
    
    response = JsonResponse({"error": "POST method required"}, status=405)
    response["Access-Control-Allow-Origin"] = "*"
    return response

urlpatterns = [
    path('admin/', admin.site.urls),
    path('health/', health_check),
    path('tenant/', tenant_info),
    path('create-tenant/', create_tenant),
    path('initialize-tenant/', initialize_tenant_data),
    path('cors/', cors_preflight),
    
    # API Management endpoints
    path('api/management/tenants/', api_management.list_tenants),
    path('api/management/tenants/create/', api_management.create_tenant),
    path('api/management/tenants/<str:tenant_name>/keys/', api_management.list_api_keys),
    path('api/management/keys/generate/', api_management.generate_api_key),
    path('api/management/keys/<uuid:key_id>/revoke/', api_management.revoke_api_key),
    
    # Storefront API endpoints
    path('api/storefront/config/', storefront_api.get_storefront_config),
    path('api/storefront/config/update/', storefront_api.update_storefront_config),
    path('api/storefront/products/', storefront_api.get_products_for_storefront),
    path('api/storefront/orders/create/', storefront_api.create_order_for_storefront),
    
    # API endpoints
    path('api/products/', api.get_products),
    path('api/products/create/', api.create_product),
    path('api/products/<str:product_id>/', api.update_product),
    path('api/products/<str:product_id>/delete/', api.delete_product),
    path('api/orders/', api.get_orders),
    path('api/orders/create/', api.create_order),
    path('api/orders/<str:order_id>/status/', api.update_order_status),
    path('api/statistics/', api.get_statistics),
    
    path('', tenant_info),
] 