"""
Lightweight Django middleware that switches the Postgres
search_path based on the sub-domain (foo.localhost -> schema "foo").
"""

from django.db import connection

def with_tenant(get_response):
    def middleware(request):
        # Priority 1: Check for API key validation (most secure)
        try:
            from django_project.api_management import validate_api_key_from_request
            tenant = validate_api_key_from_request(request)
            if tenant:
                tenant_schema = tenant.schema_name
            else:
                # Priority 2: Check for X-Tenant-ID header
                tenant_id = request.META.get('HTTP_X_TENANT_ID')
                if tenant_id:
                    tenant_schema = tenant_id.lower().replace(' ', '_')
                else:
                    # Priority 3: Fallback to host-based detection
                    host = request.get_host().split(":")[0]
                    tenant_schema = host.split(".")[0] or "default_schema"
                    
                    # If it's a cross-origin request, try to get tenant from Origin header
                    origin = request.META.get('HTTP_ORIGIN', '')
                    if origin and 'localhost' in origin:
                        origin_host = origin.replace('http://', '').replace('https://', '').split(':')[0]
                        if '.' in origin_host and origin_host != 'localhost':
                            tenant_schema = origin_host.split('.')[0]
                
                # Map 'default' to 'default_schema' for consistency
                if tenant_schema == 'default':
                    tenant_schema = 'default_schema'
        except Exception:
            # Fallback to default schema if anything goes wrong
            tenant_schema = 'default_schema'
        
        # Set the search path for this request
        with connection.cursor() as cursor:
            cursor.execute(f'SET search_path TO "{tenant_schema}", public;')
        
        return get_response(request)
    return middleware 