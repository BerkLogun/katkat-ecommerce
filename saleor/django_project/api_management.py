from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.db import connection
from .models import Tenant, ApiKey
import json
from datetime import datetime, timedelta

def add_cors_headers(response, request=None):
    # Get the origin from the request if available
    origin = request.META.get('HTTP_ORIGIN') if request else None
    
    # If we have a specific origin and it's a localhost domain (including subdomains), use it
    if origin and ('localhost' in origin or '127.0.0.1' in origin or '.localhost' in origin):
        response["Access-Control-Allow-Origin"] = origin
    else:
        response["Access-Control-Allow-Origin"] = "*"
    
    response["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
    response["Access-Control-Allow-Headers"] = "Content-Type, Authorization, X-Tenant-ID, X-API-Key, Accept, Accept-Language, User-Agent, Referer, Origin"
    response["Access-Control-Allow-Credentials"] = "true"
    response["Access-Control-Max-Age"] = "86400"
    return response

@csrf_exempt
@require_http_methods(["POST"])
def create_tenant(request):
    """Create a new tenant with schema"""
    try:
        data = json.loads(request.body)
        tenant_name = data.get('name', '').strip()
        domain = data.get('domain', '').strip()
        
        if not tenant_name:
            return add_cors_headers(JsonResponse({
                "error": "Tenant name is required"
            }, status=400), request)
        
        # Create schema name from tenant name
        schema_name = tenant_name.lower().replace(' ', '_').replace('-', '_')
        
        # Check if tenant already exists
        if Tenant.objects.filter(name=tenant_name).exists():
            return add_cors_headers(JsonResponse({
                "error": f"Tenant '{tenant_name}' already exists"
            }, status=400), request)
        
        # Create tenant record
        tenant = Tenant.objects.create(
            name=tenant_name,
            schema_name=schema_name,
            domain=domain
        )
        
        # Create database schema
        with connection.cursor() as cursor:
            cursor.execute(f'CREATE SCHEMA IF NOT EXISTS "{schema_name}";')
            
            # Set search path and create tables
            cursor.execute(f'SET search_path TO "{schema_name}", public;')
            
            # Create products table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS products (
                    id UUID PRIMARY KEY,
                    name VARCHAR(200),
                    description TEXT,
                    price DECIMAL(10,2),
                    stock INTEGER DEFAULT 0,
                    image_url VARCHAR(500),
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    is_active BOOLEAN DEFAULT TRUE
                );
            ''')
            
            # Create orders table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS orders (
                    id UUID PRIMARY KEY,
                    order_number VARCHAR(20) UNIQUE,
                    customer_email VARCHAR(254),
                    customer_name VARCHAR(200),
                    total_amount DECIMAL(10,2),
                    status VARCHAR(20) DEFAULT 'pending',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            ''')
            
            # Create order_items table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS order_items (
                    id UUID PRIMARY KEY,
                    order_id UUID REFERENCES orders(id),
                    product_id UUID REFERENCES products(id),
                    quantity INTEGER,
                    price DECIMAL(10,2)
                );
            ''')
        
        return add_cors_headers(JsonResponse({
            "success": True,
            "tenant": {
                "id": str(tenant.id),
                "name": tenant.name,
                "schema_name": tenant.schema_name,
                "domain": tenant.domain
            },
            "message": f"Tenant '{tenant_name}' created successfully"
        }), request)
        
    except Exception as e:
        return add_cors_headers(JsonResponse({
            "error": f"Failed to create tenant: {str(e)}"
        }, status=500), request)

@csrf_exempt
@require_http_methods(["POST"])
def generate_api_key(request):
    """Generate a new API key for a tenant"""
    try:
        data = json.loads(request.body)
        tenant_name = data.get('tenant_name', '').strip()
        key_name = data.get('key_name', 'Default Key').strip()
        expires_in_days = data.get('expires_in_days', 365)  # Default 1 year
        
        if not tenant_name:
            return add_cors_headers(JsonResponse({
                "error": "Tenant name is required"
            }, status=400))
        
        # Find tenant
        try:
            tenant = Tenant.objects.get(name=tenant_name)
        except Tenant.DoesNotExist:
            return add_cors_headers(JsonResponse({
                "error": f"Tenant '{tenant_name}' not found"
            }, status=404))
        
        # Generate API key
        api_key_value = ApiKey.generate_key()
        key_hash = ApiKey.hash_key(api_key_value)
        key_prefix = api_key_value[:8]
        
        # Set expiration
        expires_at = None
        if expires_in_days > 0:
            expires_at = datetime.now() + timedelta(days=expires_in_days)
        
        # Create API key record
        api_key = ApiKey.objects.create(
            tenant=tenant,
            name=key_name,
            key_hash=key_hash,
            key_prefix=key_prefix,
            expires_at=expires_at
        )
        
        return add_cors_headers(JsonResponse({
            "success": True,
            "api_key": {
                "id": str(api_key.id),
                "name": api_key.name,
                "key": api_key_value,  # Only returned once!
                "key_prefix": key_prefix,
                "expires_at": api_key.expires_at.isoformat() if api_key.expires_at else None,
                "tenant": tenant.name
            },
            "message": "API key generated successfully. Store it securely - it won't be shown again!"
        }), request)
        
    except Exception as e:
        return add_cors_headers(JsonResponse({
            "error": f"Failed to generate API key: {str(e)}"
        }, status=500), request)

@csrf_exempt
@require_http_methods(["GET"])
def list_api_keys(request):
    """List API keys for a tenant (without showing the actual keys)"""
    try:
        tenant_name = request.GET.get('tenant_name', '').strip()
        
        if not tenant_name:
            return add_cors_headers(JsonResponse({
                "error": "Tenant name is required"
            }, status=400))
        
        # Find tenant
        try:
            tenant = Tenant.objects.get(name=tenant_name)
        except Tenant.DoesNotExist:
            return add_cors_headers(JsonResponse({
                "error": f"Tenant '{tenant_name}' not found"
            }, status=404))
        
        # Get API keys
        api_keys = ApiKey.objects.filter(tenant=tenant).order_by('-created_at')
        keys_data = []
        
        for key in api_keys:
            keys_data.append({
                "id": str(key.id),
                "name": key.name,
                "key_prefix": key.key_prefix,
                "is_active": key.is_active,
                "expires_at": key.expires_at.isoformat() if key.expires_at else None,
                "last_used_at": key.last_used_at.isoformat() if key.last_used_at else None,
                "created_at": key.created_at.isoformat()
            })
        
        return add_cors_headers(JsonResponse({
            "success": True,
            "tenant": tenant.name,
            "api_keys": keys_data
        }), request)
        
    except Exception as e:
        return add_cors_headers(JsonResponse({
            "error": f"Failed to list API keys: {str(e)}"
        }, status=500), request)

@csrf_exempt
@require_http_methods(["DELETE"])
def revoke_api_key(request, key_id):
    """Revoke an API key"""
    try:
        # Find API key
        try:
            api_key = ApiKey.objects.get(id=key_id)
        except ApiKey.DoesNotExist:
            return add_cors_headers(JsonResponse({
                "error": "API key not found"
            }, status=404))
        
        # Deactivate the key
        api_key.is_active = False
        api_key.save()
        
        return add_cors_headers(JsonResponse({
            "success": True,
            "message": f"API key '{api_key.name}' has been revoked"
        }), request)
        
    except Exception as e:
        return add_cors_headers(JsonResponse({
            "error": f"Failed to revoke API key: {str(e)}"
        }, status=500), request)

@csrf_exempt
@require_http_methods(["GET"])
def list_tenants(request):
    """List all tenants"""
    try:
        tenants = Tenant.objects.filter(is_active=True).order_by('name')
        tenants_data = []
        
        for tenant in tenants:
            tenants_data.append({
                "id": str(tenant.id),
                "name": tenant.name,
                "schema_name": tenant.schema_name,
                "domain": tenant.domain,
                "created_at": tenant.created_at.isoformat(),
                "api_keys_count": tenant.api_keys.filter(is_active=True).count()
            })
        
        return add_cors_headers(JsonResponse({
            "success": True,
            "tenants": tenants_data
        }), request)
        
    except Exception as e:
        return add_cors_headers(JsonResponse({
            "error": f"Failed to list tenants: {str(e)}"
        }, status=500), request)

def validate_api_key_from_request(request):
    """Extract and validate API key from request headers"""
    # Check for API key in headers
    api_key = request.META.get('HTTP_X_API_KEY') or request.META.get('HTTP_AUTHORIZATION', '').replace('Bearer ', '')
    
    if not api_key:
        return None
    
    # Validate the API key
    tenant = ApiKey.validate_key(api_key)
    return tenant 