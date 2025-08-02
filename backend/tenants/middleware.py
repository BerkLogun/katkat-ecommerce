from django.db import connection
from django.http import JsonResponse
from django.conf import settings
from .models import Tenant, ApiKey
import logging

logger = logging.getLogger(__name__)


class TenantMiddleware:
    """Enhanced middleware for tenant isolation and routing"""
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        try:
            # Extract tenant information
            tenant = self.get_tenant_from_request(request)
            
            if tenant:
                # Set tenant context
                request.tenant = tenant
                self.set_tenant_schema(tenant.schema_name)
                
                # Add tenant info to request for logging/debugging
                request.tenant_schema = tenant.schema_name
                request.tenant_id = str(tenant.id)
            else:
                # Handle public routes or default tenant
                request.tenant = None
                request.tenant_schema = 'public'
                request.tenant_id = None
                
        except Exception as e:
            logger.error(f"Tenant middleware error: {e}")
            request.tenant = None
            request.tenant_schema = 'public'
            request.tenant_id = None
        
        response = self.get_response(request)
        
        # Add CORS headers for tenant-specific requests
        if hasattr(request, 'tenant') and request.tenant:
            response['X-Tenant-ID'] = str(request.tenant.id)
            response['X-Tenant-Name'] = request.tenant.name
        
        return response
    
    def get_tenant_from_request(self, request):
        """Extract tenant from request using multiple strategies"""
        
        # Check if this is a public route that doesn't require tenant isolation
        if self.is_public_route(request):
            return None
        
        # Strategy 1: API Key authentication (most secure)
        tenant = self.get_tenant_from_api_key(request)
        if tenant:
            return tenant
        
        # Strategy 2: X-Tenant-ID header
        tenant = self.get_tenant_from_header(request)
        if tenant:
            return tenant
        
        # Strategy 3: Host-based detection
        tenant = self.get_tenant_from_host(request)
        if tenant:
            return tenant
        
        # Strategy 4: Subdomain detection
        tenant = self.get_tenant_from_subdomain(request)
        if tenant:
            return tenant
        
        return None
    
    def is_public_route(self, request):
        """Check if the request is for a public route that doesn't require tenant isolation"""
        public_paths = [
            '/api/auth/register/',
            '/api/auth/login/',
            '/api/auth/refresh/',
            '/admin/',
        ]
        
        # Check if the request path matches any public paths
        for path in public_paths:
            if request.path.startswith(path):
                return True
        
        return False
    
    def get_tenant_from_api_key(self, request):
        """Get tenant from API key in Authorization header"""
        auth_header = request.META.get('HTTP_AUTHORIZATION', '')
        if auth_header.startswith('Bearer '):
            api_key = auth_header.split(' ')[1]
            return ApiKey.validate_key(api_key)
        return None
    
    def get_tenant_from_header(self, request):
        """Get tenant from X-Tenant-ID header"""
        tenant_id = request.META.get('HTTP_X_TENANT_ID')
        if tenant_id:
            try:
                return Tenant.objects.get(id=tenant_id, is_active=True)
            except Tenant.DoesNotExist:
                return None
        return None
    
    def get_tenant_from_host(self, request):
        """Get tenant from host header"""
        host = request.get_host().split(':')[0]
        
        # Check for exact domain match
        try:
            return Tenant.objects.get(domain=host, is_active=True)
        except Tenant.DoesNotExist:
            pass
        
        return None
    
    def get_tenant_from_subdomain(self, request):
        """Get tenant from subdomain"""
        host = request.get_host().split(':')[0]
        
        # Handle localhost subdomains (e.g., tenant.localhost)
        if 'localhost' in host or '127.0.0.1' in host:
            parts = host.split('.')
            if len(parts) >= 2:
                subdomain = parts[0]
                if subdomain not in ['localhost', '127', 'www']:
                    try:
                        return Tenant.objects.get(subdomain=subdomain, is_active=True)
                    except Tenant.DoesNotExist:
                        pass
        
        return None
    
    def set_tenant_schema(self, schema_name):
        """Set the database search path for the tenant"""
        try:
            with connection.cursor() as cursor:
                cursor.execute(f'SET search_path TO "{schema_name}", public;')
        except Exception as e:
            logger.error(f"Failed to set tenant schema {schema_name}: {e}")
            # Fallback to public schema
            with connection.cursor() as cursor:
                cursor.execute('SET search_path TO public;')


class TenantContextMiddleware:
    """Middleware to add tenant context to all requests"""
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        # Add tenant context to request
        if hasattr(request, 'tenant') and request.tenant:
            # Add tenant info to request for easy access
            request.tenant_info = {
                'id': str(request.tenant.id),
                'name': request.tenant.name,
                'schema_name': request.tenant.schema_name,
                'plan_type': request.tenant.plan_type,
                'is_premium': request.tenant.is_premium,
            }
        else:
            request.tenant_info = None
        
        response = self.get_response(request)
        return response 