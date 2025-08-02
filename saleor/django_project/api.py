from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.db import connection
from django.db.models import Sum, Count
from django.core.serializers import serialize
import json
from .models import Product, Order, OrderItem
import uuid
from decimal import Decimal

def get_tenant_from_request(request):
    """Extract tenant from request headers or fallback to origin"""
    # Priority 1: Check for API key validation (most secure)
    from .api_management import validate_api_key_from_request
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

def add_cors_headers(response):
    response["Access-Control-Allow-Origin"] = "*"
    response["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
    response["Access-Control-Allow-Headers"] = "Content-Type, Authorization, X-Tenant-ID, X-API-Key"
    return response

@csrf_exempt
@require_http_methods(["GET"])
def get_products(request):
    try:
        # Get tenant and set schema
        tenant = get_tenant_from_request(request)
        set_tenant_schema(tenant)
        
        products = Product.objects.filter(is_active=True)
        products_data = []
        for product in products:
            products_data.append({
                'id': str(product.id),
                'name': product.name,
                'description': product.description,
                'price': float(product.price),
                'stock': product.stock,
                'image_url': product.image_url,
                'created_at': product.created_at.isoformat(),
            })
        
        response = JsonResponse({'products': products_data})
        return add_cors_headers(response)
    except Exception as e:
        response = JsonResponse({'error': str(e)}, status=500)
        return add_cors_headers(response)

@csrf_exempt
@require_http_methods(["POST"])
def create_product(request):
    try:
        # Get tenant and set schema
        tenant = get_tenant_from_request(request)
        set_tenant_schema(tenant)
        
        data = json.loads(request.body)
        product = Product.objects.create(
            name=data['name'],
            description=data.get('description', ''),
            price=Decimal(data['price']),
            stock=data.get('stock', 0),
            image_url=data.get('image_url', ''),
        )
        
        response = JsonResponse({
            'success': True,
            'product': {
                'id': str(product.id),
                'name': product.name,
                'description': product.description,
                'price': float(product.price),
                'stock': product.stock,
                'image_url': product.image_url,
            }
        })
        return add_cors_headers(response)
    except Exception as e:
        response = JsonResponse({'error': str(e)}, status=500)
        return add_cors_headers(response)

@csrf_exempt
@require_http_methods(["PUT"])
def update_product(request, product_id):
    try:
        # Get tenant and set schema
        tenant = get_tenant_from_request(request)
        set_tenant_schema(tenant)
        
        data = json.loads(request.body)
        product = Product.objects.get(id=product_id)
        
        if 'name' in data:
            product.name = data['name']
        if 'description' in data:
            product.description = data['description']
        if 'price' in data:
            product.price = Decimal(data['price'])
        if 'stock' in data:
            product.stock = data['stock']
        if 'image_url' in data:
            product.image_url = data['image_url']
        if 'is_active' in data:
            product.is_active = data['is_active']
            
        product.save()
        
        response = JsonResponse({
            'success': True,
            'product': {
                'id': str(product.id),
                'name': product.name,
                'description': product.description,
                'price': float(product.price),
                'stock': product.stock,
                'image_url': product.image_url,
                'is_active': product.is_active,
            }
        })
        return add_cors_headers(response)
    except Product.DoesNotExist:
        response = JsonResponse({'error': 'Product not found'}, status=404)
        return add_cors_headers(response)
    except Exception as e:
        response = JsonResponse({'error': str(e)}, status=500)
        return add_cors_headers(response)

@csrf_exempt
@require_http_methods(["DELETE"])
def delete_product(request, product_id):
    try:
        # Get tenant and set schema
        tenant = get_tenant_from_request(request)
        set_tenant_schema(tenant)
        
        product = Product.objects.get(id=product_id)
        product.is_active = False
        product.save()
        
        response = JsonResponse({'success': True, 'message': 'Product deleted'})
        return add_cors_headers(response)
    except Product.DoesNotExist:
        response = JsonResponse({'error': 'Product not found'}, status=404)
        return add_cors_headers(response)
    except Exception as e:
        response = JsonResponse({'error': str(e)}, status=500)
        return add_cors_headers(response)

@csrf_exempt
@require_http_methods(["GET"])
def get_orders(request):
    try:
        # Get tenant and set schema
        tenant = get_tenant_from_request(request)
        set_tenant_schema(tenant)
        
        orders = Order.objects.all().order_by('-created_at')
        orders_data = []
        for order in orders:
            items_data = []
            for item in order.items.all():
                items_data.append({
                    'product_name': item.product.name,
                    'quantity': item.quantity,
                    'price': float(item.price),
                })
            
            orders_data.append({
                'id': str(order.id),
                'order_number': order.order_number,
                'customer_name': order.customer_name,
                'customer_email': order.customer_email,
                'total_amount': float(order.total_amount),
                'status': order.status,
                'created_at': order.created_at.isoformat(),
                'items': items_data,
            })
        
        response = JsonResponse({'orders': orders_data})
        return add_cors_headers(response)
    except Exception as e:
        response = JsonResponse({'error': str(e)}, status=500)
        return add_cors_headers(response)

@csrf_exempt
@require_http_methods(["POST"])
def create_order(request):
    try:
        # Get tenant and set schema
        tenant = get_tenant_from_request(request)
        set_tenant_schema(tenant)
        
        data = json.loads(request.body)
        
        # Generate order number
        order_number = f"ORD-{uuid.uuid4().hex[:8].upper()}"
        
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
        
        response = JsonResponse({
            'success': True,
            'order': {
                'id': str(order.id),
                'order_number': order.order_number,
                'total_amount': float(order.total_amount),
            }
        })
        return add_cors_headers(response)
    except Exception as e:
        response = JsonResponse({'error': str(e)}, status=500)
        return add_cors_headers(response)

@csrf_exempt
@require_http_methods(["PUT"])
def update_order_status(request, order_id):
    try:
        # Get tenant and set schema
        tenant = get_tenant_from_request(request)
        set_tenant_schema(tenant)
        
        data = json.loads(request.body)
        order = Order.objects.get(id=order_id)
        order.status = data['status']
        order.save()
        
        response = JsonResponse({
            'success': True,
            'order': {
                'id': str(order.id),
                'order_number': order.order_number,
                'status': order.status,
            }
        })
        return add_cors_headers(response)
    except Order.DoesNotExist:
        response = JsonResponse({'error': 'Order not found'}, status=404)
        return add_cors_headers(response)
    except Exception as e:
        response = JsonResponse({'error': str(e)}, status=500)
        return add_cors_headers(response)

@csrf_exempt
@require_http_methods(["GET"])
def get_statistics(request):
    try:
        # Get tenant and set schema
        tenant = get_tenant_from_request(request)
        set_tenant_schema(tenant)
        
        # Total products
        total_products = Product.objects.filter(is_active=True).count()
        
        # Total orders
        total_orders = Order.objects.count()
        
        # Total revenue
        total_revenue = Order.objects.filter(status__in=['delivered', 'shipped']).aggregate(
            total=Sum('total_amount')
        )['total'] or Decimal('0.00')
        
        # Orders by status
        orders_by_status = Order.objects.values('status').annotate(
            count=Count('id')
        )
        
        # Recent orders
        recent_orders = Order.objects.order_by('-created_at')[:5]
        recent_orders_data = []
        for order in recent_orders:
            recent_orders_data.append({
                'order_number': order.order_number,
                'customer_name': order.customer_name,
                'total_amount': float(order.total_amount),
                'status': order.status,
                'created_at': order.created_at.isoformat(),
            })
        
        # Top selling products
        top_products = Product.objects.filter(
            orderitem__order__status__in=['delivered', 'shipped']
        ).annotate(
            total_sold=Sum('orderitem__quantity')
        ).order_by('-total_sold')[:5]
        
        top_products_data = []
        for product in top_products:
            top_products_data.append({
                'name': product.name,
                'total_sold': product.total_sold or 0,
            })
        
        response = JsonResponse({
            'statistics': {
                'total_products': total_products,
                'total_orders': total_orders,
                'total_revenue': float(total_revenue),
                'orders_by_status': list(orders_by_status),
                'recent_orders': recent_orders_data,
                'top_products': top_products_data,
            }
        })
        return add_cors_headers(response)
    except Exception as e:
        response = JsonResponse({'error': str(e)}, status=500)
        return add_cors_headers(response) 